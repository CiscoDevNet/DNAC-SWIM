## Introduction
SWIM (SoftWare Image Management) API allow for the distribution and activation of software 
images on Cisco network devices.

This service is hosted on Cisco DNA Center.  Images are stored locally on Cisco DNA Center and https is used to distribute them.
Images are distributed to devices by either HTTPS or SFTP.

## using IP address too
As of May 2019, in addition to a tagm you can also provide a list of IPs sepperated by ','.  make sure to remove spaces, otherwise the shell will get upset.
If you provide both a tag and a list of ips, only unique will be used.

## list_images.py
provides a list of all of the images on DNAC

```buildoutcfg
$ ./list_images.py 
https://sandboxdnac.cisco.com:8080/api/v1/image/importation
Name                                         Version        FileSize          Family         importSourceType
cat3k_caa-universalk9.16.06.02s.SPA.bin      16.6.2s        409953451 bytes   CAT3K_CAA      FILESYSTEM
cat9k_iosxe.16.06.02s.SPA.bin                16.6.2s        596391064 bytes   CAT9K          FILESYSTEM

```
## Distribute.py
takes a tag and an imagename.  If an image is not supplied, the "golden image" for the device will be used.
Any devices with the tag associated with them will have the image distributed to them.  At present there is no
checking in the script, so you need to be careful (or extend the script) 


```buildoutcfg
 ./distribute.py --tag upgrade9k --image cat9k_iosxe.16.06.02s.SPA.bin
https://sandboxdnac.cisco.com:8080/api/v1/tag/association?tag=upgrade9k&resourceType=network-device
https://sandboxdnac.cisco.com:8080/api/v1/image/importation?name=cat9k_iosxe.16.06.02s.SPA.bin
https://sandboxdnac.cisco.com:8080/api/v1/image/importation/dbd0f3d3-c24e-4e70-9391-0ab38b3cfc32
CAT9K
https://sandboxdnac.cisco.com:8080/api/v1/network-device/74b69532-5dc3-45a1-a0dd-6d1d10051f27
Cisco Catalyst 9300 Series Switches
Waiting for Task a64bfaea-12f7-442d-9de7-ecede961b226
Task=a64bfaea-12f7-442d-9de7-ecede961b226 has not completed yet. Sleeping 60 seconds...
Task=a64bfaea-12f7-442d-9de7-ecede961b226 has not completed yet. Sleeping 60 seconds...
Task=a64bfaea-12f7-442d-9de7-ecede961b226 has not completed yet. Sleeping 60 seconds...
Task=a64bfaea-12f7-442d-9de7-ecede961b226 has not completed yet. Sleeping 60 seconds...
Task=a64bfaea-12f7-442d-9de7-ecede961b226 has not completed yet. Sleeping 60 seconds...
Task=a64bfaea-12f7-442d-9de7-ecede961b226 has not completed yet. Sleeping 60 seconds...
Task=a64bfaea-12f7-442d-9de7-ecede961b226 has not completed yet. Sleeping 60 seconds...
Task=a64bfaea-12f7-442d-9de7-ecede961b226 has not completed yet. Sleeping 60 seconds...
{'version': 1517125988427, 'endTime': 1517125989689, 'startTime': 1517125988389, 'serviceType': 'Swim Service', 'rootId': 'a64bfaea-12f7-442d-9de7-ecede961b226', 'id': 'a64bfaea-12f7-442d-9de7-ecede961b226', 'progress': 'completed successfully.  Success = 1, Failure = 0, Running = 0, Pending = 0, Total = 1', 'additionalStatusURL': '/api/v1/image/task?taskUuid=a64bfaea-12f7-442d-9de7-ecede961b226', 'isError': False, 'lastUpdate': 1517125988427}
https://sandboxdnac.cisco.com:8080/api/v1/image/task?taskUuid=a64bfaea-12f7-442d-9de7-ecede961b226
{
  "version": "1.0",
  "response": [
    {
      "deviceIp": "10.10.22.70",
      "taskType": "distribute",
      "taskStatus": "success",
      "imageName": "cat9k_iosxe.16.06.02s.SPA.bin",
      "operation": "",
      "logDetails": "",
      "taskUuid": "a64bfaea-12f7-442d-9de7-ecede961b226",
      "unitTaskUuid": "1c4f99f8-ef94-4339-87c5-e45a23e2f882",
      "deviceTaskUuid": "20c87cbd-8ea7-46f9-82a8-3f02ace98513",
      "startTime": "1517125988427",
      "deviceId": "74b69532-5dc3-45a1-a0dd-6d1d10051f27",
      "completionTime": "1517125989494"
    }
  ]
}

```
## delete.py
used to delete an image from a device.  This could be used to clean up flash space.  In this case we are using 
it to clean up and allow another image to be pushed.

```buildoutcfg
$ ./delete.py --tag upgrade9k --image cat9k_iosxe.16.06.02s.SPA.bin
https://sandboxdnac.cisco.com:8080/api/v1/tag/association?tag=upgrade9k&resourceType=network-device
Waiting for Task 3a455f95-1a87-4ae7-b5a8-c8cd0949fdf8
{'data': 'delete-image-device', 'isError': False, 'startTime': 1517126153695, 'rootId': '3a455f95-1a87-4ae7-b5a8-c8cd0949fdf8', 'id': '3a455f95-1a87-4ae7-b5a8-c8cd0949fdf8', 'progress': 'completed successfully.  Success = 1, Failure = 0, Running = 0, Pending = 0, Total = 1', 'version': 1517126153695, 'endTime': 1517126154725, 'serviceType': 'Swim Service'}

```

## activate.py
This works in the same way as distribution.  Activates an image once distributed.  Can take tag or a list of IP or both.
As with distritution, you can leave image blank and the golden image will be used.

However, if you are distributing a non-golden image, you will need to specify the same golden image to activate.
If you are activating the golden image, then no need to specify an image.

