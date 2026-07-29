using System;
using System.IO;
using System.Linq;
using System.Drawing;
using System.Drawing.Imaging;
using Microsoft.Kinect;

class KinectBridge
{
    static KinectSensor sensor;
    static byte[] colorPixels;
    static short[] depthPixels;

    static string liveDir = Path.Combine("deployment", "live");
    static string rgbPath = Path.Combine(liveDir, "rgb.png");
    static string depthPath = Path.Combine(liveDir, "depth.bin");

    static void Main()
    {
        Directory.CreateDirectory(liveDir);

        sensor = KinectSensor.KinectSensors.FirstOrDefault(s => s.Status == KinectStatus.Connected);

        if (sensor == null)
        {
            Console.WriteLine("No Kinect sensor found.");
            return;
        }

        sensor.ColorStream.Enable(ColorImageFormat.RgbResolution640x480Fps30);
        sensor.DepthStream.Enable(DepthImageFormat.Resolution640x480Fps30);

        colorPixels = new byte[sensor.ColorStream.FramePixelDataLength];
        depthPixels = new short[sensor.DepthStream.FramePixelDataLength];

        sensor.ColorFrameReady += ColorFrameReady;
        sensor.DepthFrameReady += DepthFrameReady;

        sensor.Start();

        Console.WriteLine("Kinect bridge running.");
        Console.WriteLine("Saving:");
        Console.WriteLine(rgbPath);
        Console.WriteLine(depthPath);
        Console.WriteLine("Press ENTER to stop.");

        Console.ReadLine();

        sensor.Stop();
    }

    static void ColorFrameReady(object sender, ColorImageFrameReadyEventArgs e)
    {
        using (ColorImageFrame frame = e.OpenColorImageFrame())
        {
            if (frame == null) return;

            frame.CopyPixelDataTo(colorPixels);

            using (Bitmap bmp = new Bitmap(frame.Width, frame.Height, PixelFormat.Format32bppRgb))
            {
                BitmapData data = bmp.LockBits(
                    new Rectangle(0, 0, frame.Width, frame.Height),
                    ImageLockMode.WriteOnly,
                    bmp.PixelFormat
                );

                System.Runtime.InteropServices.Marshal.Copy(colorPixels, 0, data.Scan0, colorPixels.Length);
                bmp.UnlockBits(data);

                SaveAtomic(bmp, rgbPath);
            }
        }
    }

    static void DepthFrameReady(object sender, DepthImageFrameReadyEventArgs e)
    {
        using (DepthImageFrame frame = e.OpenDepthImageFrame())
        {
            if (frame == null) return;

            frame.CopyPixelDataTo(depthPixels);

            ushort[] depthMm = new ushort[depthPixels.Length];

            for (int i = 0; i < depthPixels.Length; i++)
            {
                depthMm[i] = (ushort)(depthPixels[i] >> DepthImageFrame.PlayerIndexBitmaskWidth);
            }

            SaveDepthAtomic(depthMm, depthPath);
        }
    }

    static void SaveAtomic(Bitmap bmp, string path)
    {
        string temp = path + ".tmp";

        try
        {
            bmp.Save(temp, ImageFormat.Png);

            if (File.Exists(path))
            {
                File.Delete(path);
            }

            File.Move(temp, path);
        }
        catch (Exception ex)
        {
            Console.WriteLine("Save failed for " + path + ": " + ex.Message);
            try
            {
                if (File.Exists(temp)) File.Delete(temp);
            }
            catch { }
        }
    }
    static void SaveDepthAtomic(ushort[] depthMm, string path)
    {
        string temp = path + ".tmp";

        try
        {
            byte[] bytes = new byte[depthMm.Length * 2];
            Buffer.BlockCopy(depthMm, 0, bytes, 0, bytes.Length);

            File.WriteAllBytes(temp, bytes);

            if (File.Exists(path))
            {
                File.Delete(path);
            }

            File.Move(temp, path);
        }
        catch (Exception ex)
        {
            Console.WriteLine("Depth save failed for " + path + ": " + ex.Message);

            try
            {
                if (File.Exists(temp)) File.Delete(temp);
            }
            catch { }
        }
    }
}