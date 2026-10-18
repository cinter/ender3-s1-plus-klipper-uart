# Optional webcam

[crowsnest.conf.example](crowsnest.conf.example) is a selected example with a placeholder device path. Find your own camera under /dev/v4l/by-id and set its supported resolution/frame rate. Do not replace an unrelated working camera configuration wholesale.

The observed camera identifies itself over USB as NexiGo N60 FHD. A 720p stream worked in the diagnostic setup; a prior 1080p attempt stopped during USB experiments. This does not establish a general resolution limit for the camera.

On stock display-cable power, unplugging the camera coincided with the end of repeated undervoltage warnings over the next 8.5 minutes. Validate [power](../../docs/power.md) under the full intended load before treating a camera stream as a stable baseline.

Configure the corresponding camera stream in Mainsail. Optional remote access is configured separately and no account details are included.
