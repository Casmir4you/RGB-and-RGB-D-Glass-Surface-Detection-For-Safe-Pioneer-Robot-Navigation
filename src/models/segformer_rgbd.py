from __future__ import annotations

import torch
from torch import nn
from transformers import SegformerConfig, SegformerForSemanticSegmentation


def build_segformer(
    model_name: str = "nvidia/mit-b0",
    num_classes: int = 2,
    in_channels: int = 3,
    ignore_index: int = 255,
    pretrained: bool = True,
) -> SegformerForSemanticSegmentation:
    """
    Build SegFormer for RGB or RGB-D semantic segmentation.

    For RGB-D, the first patch embedding convolution is changed from 3 to 4 input channels.
    The depth-channel weights are initialised using the mean of the pretrained RGB weights.
    """
    if pretrained:
        model = SegformerForSemanticSegmentation.from_pretrained(
            model_name,
            num_labels=num_classes,
            ignore_mismatched_sizes=True,
        )
    else:
        config = SegformerConfig.from_pretrained(model_name, num_labels=num_classes)
        model = SegformerForSemanticSegmentation(config)

    model.config.num_labels = num_classes
    model.config.semantic_loss_ignore_index = ignore_index

    if in_channels == 4:
        model = convert_segformer_to_rgbd(model)
    elif in_channels != 3:
        raise ValueError("This template supports only 3-channel RGB or 4-channel RGB-D input.")

    return model


def convert_segformer_to_rgbd(model: SegformerForSemanticSegmentation) -> SegformerForSemanticSegmentation:
    """Modify SegFormer's first patch embedding layer to accept RGB-D input."""

    old_conv = None
    conv_name = None

    for name, module in model.named_modules():
        if isinstance(module, nn.Conv2d) and module.in_channels == 3:
            old_conv = module
            conv_name = name
            break

    if old_conv is None:
        raise AttributeError("Could not find a 3-channel Conv2d layer to convert to RGB-D.")

    new_conv = nn.Conv2d(
        in_channels=4,
        out_channels=old_conv.out_channels,
        kernel_size=old_conv.kernel_size,
        stride=old_conv.stride,
        padding=old_conv.padding,
        dilation=old_conv.dilation,
        groups=old_conv.groups,
        bias=old_conv.bias is not None,
        padding_mode=old_conv.padding_mode,
    )

    with torch.no_grad():
        new_conv.weight[:, :3, :, :] = old_conv.weight
        new_conv.weight[:, 3:4, :, :] = old_conv.weight.mean(dim=1, keepdim=True)

        if old_conv.bias is not None:
            new_conv.bias.copy_(old_conv.bias)

    # Replace the original layer inside the model
    parent_name, child_name = conv_name.rsplit(".", 1)
    parent_module = model

    for attr in parent_name.split("."):
        parent_module = getattr(parent_module, attr)

    setattr(parent_module, child_name, new_conv)

    print(f"Converted first patch convolution to RGB-D: {conv_name}")
    print(f"New input channels: {new_conv.in_channels}")

    return model