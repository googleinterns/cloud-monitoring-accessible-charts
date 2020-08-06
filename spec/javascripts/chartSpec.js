describe("Suite for chart", function() {
  const points = [{
    "interval": {
      "startTime": "2020-06-26T11:29:00Z",
      "endTime": "2020-06-26T11:30:00Z",
    },
    "value": {
      "doubleValue": 13.974581782938913,
    },
  },
  {
    "interval": {
      "startTime": "2020-06-26T11:28:00Z",
      "endTime": "2020-06-26T11:29:00Z",
    },
    "value": {
      "doubleValue": 14.061566321528517,
    },
  }];

  const newPoints = [[13.974581782938913, 14.061566321528517],
    [new Date("2020-06-26T11:29:00Z"), new Date("2020-06-26T11:28:00Z")]];

  const data = [[10, 20], [100, 300]];

  const chartData = {
    "timeSeries": [
      {
        "metric": {
          "labels": {
            "instance_name": "gke-demo-default-pool-272cd19c-8mr4",
          },
          "type": "compute.googleapis.com/instance/cpu/usage_time",
        },
        "resource": {
          "type": "gce_instance",
          "labels": {
            "instance_id": "1575673166315746232",
            "project_id": "rnataly-hipstershop",
            "zone": "us-central1-a",
          },
        },
        "metricKind": "DELTA",
        "valueType": "DOUBLE",
        "points": [
          {
            "interval": {
              "startTime": "2020-06-26T11:29:00Z",
              "endTime": "2020-06-26T11:30:00Z",
            },
            "value": {
              "doubleValue": 13.974581782938913,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:28:00Z",
              "endTime": "2020-06-26T11:29:00Z",
            },
            "value": {
              "doubleValue": 14.061566321528517,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:27:00Z",
              "endTime": "2020-06-26T11:28:00Z",
            },
            "value": {
              "doubleValue": 13.743431459646672,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:26:00Z",
              "endTime": "2020-06-26T11:27:00Z",
            },
            "value": {
              "doubleValue": 13.592257376949419,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:25:00Z",
              "endTime": "2020-06-26T11:26:00Z",
            },
            "value": {
              "doubleValue": 13.723796155012678,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:24:00Z",
              "endTime": "2020-06-26T11:25:00Z",
            },
            "value": {
              "doubleValue": 13.525640773121268,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:23:00Z",
              "endTime": "2020-06-26T11:24:00Z",
            },
            "value": {
              "doubleValue": 13.838546073748148,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:22:00Z",
              "endTime": "2020-06-26T11:23:00Z",
            },
            "value": {
              "doubleValue": 13.803581298154313,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:21:00Z",
              "endTime": "2020-06-26T11:22:00Z",
            },
            "value": {
              "doubleValue": 13.610266152449185,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:20:00Z",
              "endTime": "2020-06-26T11:21:00Z",
            },
            "value": {
              "doubleValue": 13.847093966542161,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:19:00Z",
              "endTime": "2020-06-26T11:20:00Z",
            },
            "value": {
              "doubleValue": 13.862572314174031,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:18:00Z",
              "endTime": "2020-06-26T11:19:00Z",
            },
            "value": {
              "doubleValue": 14.233789438934764,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:17:00Z",
              "endTime": "2020-06-26T11:18:00Z",
            },
            "value": {
              "doubleValue": 13.629662147257477,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:16:00Z",
              "endTime": "2020-06-26T11:17:00Z",
            },
            "value": {
              "doubleValue": 13.676325370164705,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:15:00Z",
              "endTime": "2020-06-26T11:16:00Z",
            },
            "value": {
              "doubleValue": 13.828412471397314,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:14:00Z",
              "endTime": "2020-06-26T11:15:00Z",
            },
            "value": {
              "doubleValue": 13.9328589009383,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:13:00Z",
              "endTime": "2020-06-26T11:14:00Z",
            },
            "value": {
              "doubleValue": 14.26328494954214,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:12:00Z",
              "endTime": "2020-06-26T11:13:00Z",
            },
            "value": {
              "doubleValue": 13.78840199172555,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:11:00Z",
              "endTime": "2020-06-26T11:12:00Z",
            },
            "value": {
              "doubleValue": 13.938631665354478,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:10:00Z",
              "endTime": "2020-06-26T11:11:00Z",
            },
            "value": {
              "doubleValue": 13.844251540474943,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:09:00Z",
              "endTime": "2020-06-26T11:10:00Z",
            },
            "value": {
              "doubleValue": 13.837323838670272,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:08:00Z",
              "endTime": "2020-06-26T11:09:00Z",
            },
            "value": {
              "doubleValue": 14.193188953911886,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:07:00Z",
              "endTime": "2020-06-26T11:08:00Z",
            },
            "value": {
              "doubleValue": 14.012731409369735,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:06:00Z",
              "endTime": "2020-06-26T11:07:00Z",
            },
            "value": {
              "doubleValue": 14.016566243648413,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:05:00Z",
              "endTime": "2020-06-26T11:06:00Z",
            },
            "value": {
              "doubleValue": 13.868208742584102,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:04:00Z",
              "endTime": "2020-06-26T11:05:00Z",
            },
            "value": {
              "doubleValue": 13.95575595475384,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:03:00Z",
              "endTime": "2020-06-26T11:04:00Z",
            },
            "value": {
              "doubleValue": 13.998159647453576,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:02:00Z",
              "endTime": "2020-06-26T11:03:00Z",
            },
            "value": {
              "doubleValue": 13.748875694800518,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:01:00Z",
              "endTime": "2020-06-26T11:02:00Z",
            },
            "value": {
              "doubleValue": 13.643702346336795,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:00:00Z",
              "endTime": "2020-06-26T11:01:00Z",
            },
            "value": {
              "doubleValue": 13.628257150092395,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:59:00Z",
              "endTime": "2020-06-26T11:00:00Z",
            },
            "value": {
              "doubleValue": 13.695537894018344,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:58:00Z",
              "endTime": "2020-06-26T10:59:00Z",
            },
            "value": {
              "doubleValue": 13.855217666525277,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:57:00Z",
              "endTime": "2020-06-26T10:58:00Z",
            },
            "value": {
              "doubleValue": 13.471469594427617,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:56:00Z",
              "endTime": "2020-06-26T10:57:00Z",
            },
            "value": {
              "doubleValue": 13.711224644415779,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:55:00Z",
              "endTime": "2020-06-26T10:56:00Z",
            },
            "value": {
              "doubleValue": 13.581216214210144,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:54:00Z",
              "endTime": "2020-06-26T10:55:00Z",
            },
            "value": {
              "doubleValue": 13.673948489449685,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:53:00Z",
              "endTime": "2020-06-26T10:54:00Z",
            },
            "value": {
              "doubleValue": 13.912590933192405,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:52:00Z",
              "endTime": "2020-06-26T10:53:00Z",
            },
            "value": {
              "doubleValue": 13.472205722500803,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:51:00Z",
              "endTime": "2020-06-26T10:52:00Z",
            },
            "value": {
              "doubleValue": 13.618024769340991,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:50:00Z",
              "endTime": "2020-06-26T10:51:00Z",
            },
            "value": {
              "doubleValue": 13.695798816013848,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:49:00Z",
              "endTime": "2020-06-26T10:50:00Z",
            },
            "value": {
              "doubleValue": 13.924813756995718,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:48:00Z",
              "endTime": "2020-06-26T10:49:00Z",
            },
            "value": {
              "doubleValue": 13.96763904877298,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:47:00Z",
              "endTime": "2020-06-26T10:48:00Z",
            },
            "value": {
              "doubleValue": 13.847135773350601,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:46:00Z",
              "endTime": "2020-06-26T10:47:00Z",
            },
            "value": {
              "doubleValue": 13.791620525924372,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:45:00Z",
              "endTime": "2020-06-26T10:46:00Z",
            },
            "value": {
              "doubleValue": 13.771454609101056,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:44:00Z",
              "endTime": "2020-06-26T10:45:00Z",
            },
            "value": {
              "doubleValue": 13.840821699253866,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:43:00Z",
              "endTime": "2020-06-26T10:44:00Z",
            },
            "value": {
              "doubleValue": 14.195555541024078,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:42:00Z",
              "endTime": "2020-06-26T10:43:00Z",
            },
            "value": {
              "doubleValue": 13.72068004294124,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:41:00Z",
              "endTime": "2020-06-26T10:42:00Z",
            },
            "value": {
              "doubleValue": 13.79964223888237,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:40:00Z",
              "endTime": "2020-06-26T10:41:00Z",
            },
            "value": {
              "doubleValue": 13.497813250360196,
            },
          },
        ]},
      {
        "metric": {
          "labels": {
            "instance_name": "gke-demo-default-pool-272cd19c-rprw",
          },
          "type": "compute.googleapis.com/instance/cpu/usage_time",
        },
        "resource": {
          "type": "gce_instance",
          "labels": {
            "instance_id": "2191822968372163512",
            "zone": "us-central1-a",
            "project_id": "rnataly-hipstershop",
          },
        },
        "metricKind": "DELTA",
        "valueType": "DOUBLE",
        "points": [
          {
            "interval": {
              "startTime": "2020-06-26T11:29:00Z",
              "endTime": "2020-06-26T11:30:00Z",
            },
            "value": {
              "doubleValue": 14.905993941792985,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:28:00Z",
              "endTime": "2020-06-26T11:29:00Z",
            },
            "value": {
              "doubleValue": 14.877986554842209,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:27:00Z",
              "endTime": "2020-06-26T11:28:00Z",
            },
            "value": {
              "doubleValue": 14.704301676014438,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:26:00Z",
              "endTime": "2020-06-26T11:27:00Z",
            },
            "value": {
              "doubleValue": 14.608741502008343,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:25:00Z",
              "endTime": "2020-06-26T11:26:00Z",
            },
            "value": {
              "doubleValue": 14.461994076387782,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:24:00Z",
              "endTime": "2020-06-26T11:25:00Z",
            },
            "value": {
              "doubleValue": 14.554778686506324,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:23:00Z",
              "endTime": "2020-06-26T11:24:00Z",
            },
            "value": {
              "doubleValue": 14.571881430390931,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:22:00Z",
              "endTime": "2020-06-26T11:23:00Z",
            },
            "value": {
              "doubleValue": 15.097902442423219,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:21:00Z",
              "endTime": "2020-06-26T11:22:00Z",
            },
            "value": {
              "doubleValue": 14.383142445134581,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:20:00Z",
              "endTime": "2020-06-26T11:21:00Z",
            },
            "value": {
              "doubleValue": 14.625989509309875,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:19:00Z",
              "endTime": "2020-06-26T11:20:00Z",
            },
            "value": {
              "doubleValue": 14.761278051439149,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:18:00Z",
              "endTime": "2020-06-26T11:19:00Z",
            },
            "value": {
              "doubleValue": 14.627460330491886,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:17:00Z",
              "endTime": "2020-06-26T11:18:00Z",
            },
            "value": {
              "doubleValue": 14.890439331604284,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:16:00Z",
              "endTime": "2020-06-26T11:17:00Z",
            },
            "value": {
              "doubleValue": 14.754763530814671,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:15:00Z",
              "endTime": "2020-06-26T11:16:00Z",
            },
            "value": {
              "doubleValue": 14.581941867108981,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:14:00Z",
              "endTime": "2020-06-26T11:15:00Z",
            },
            "value": {
              "doubleValue": 14.673136923804122,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:13:00Z",
              "endTime": "2020-06-26T11:14:00Z",
            },
            "value": {
              "doubleValue": 14.807364885811694,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:12:00Z",
              "endTime": "2020-06-26T11:13:00Z",
            },
            "value": {
              "doubleValue": 14.951152008790814,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:11:00Z",
              "endTime": "2020-06-26T11:12:00Z",
            },
            "value": {
              "doubleValue": 14.623795051200432,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:10:00Z",
              "endTime": "2020-06-26T11:11:00Z",
            },
            "value": {
              "doubleValue": 14.78406578025897,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:09:00Z",
              "endTime": "2020-06-26T11:10:00Z",
            },
            "value": {
              "doubleValue": 14.577352219719614,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:08:00Z",
              "endTime": "2020-06-26T11:09:00Z",
            },
            "value": {
              "doubleValue": 14.788081516613602,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:07:00Z",
              "endTime": "2020-06-26T11:08:00Z",
            },
            "value": {
              "doubleValue": 14.905295782758913,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:06:00Z",
              "endTime": "2020-06-26T11:07:00Z",
            },
            "value": {
              "doubleValue": 14.837860780338815,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:05:00Z",
              "endTime": "2020-06-26T11:06:00Z",
            },
            "value": {
              "doubleValue": 14.711469210968062,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:04:00Z",
              "endTime": "2020-06-26T11:05:00Z",
            },
            "value": {
              "doubleValue": 14.48158425463771,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:03:00Z",
              "endTime": "2020-06-26T11:04:00Z",
            },
            "value": {
              "doubleValue": 14.739935990728554,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:02:00Z",
              "endTime": "2020-06-26T11:03:00Z",
            },
            "value": {
              "doubleValue": 14.801219836386736,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:01:00Z",
              "endTime": "2020-06-26T11:02:00Z",
            },
            "value": {
              "doubleValue": 14.512326342039159,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T11:00:00Z",
              "endTime": "2020-06-26T11:01:00Z",
            },
            "value": {
              "doubleValue": 14.353505942068296,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:59:00Z",
              "endTime": "2020-06-26T11:00:00Z",
            },
            "value": {
              "doubleValue": 14.504045780784509,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:58:00Z",
              "endTime": "2020-06-26T10:59:00Z",
            },
            "value": {
              "doubleValue": 14.635035014165624,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:57:00Z",
              "endTime": "2020-06-26T10:58:00Z",
            },
            "value": {
              "doubleValue": 14.66983647170855,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:56:00Z",
              "endTime": "2020-06-26T10:57:00Z",
            },
            "value": {
              "doubleValue": 14.330551600076433,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:55:00Z",
              "endTime": "2020-06-26T10:56:00Z",
            },
            "value": {
              "doubleValue": 14.78968462820194,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:54:00Z",
              "endTime": "2020-06-26T10:55:00Z",
            },
            "value": {
              "doubleValue": 14.68138280997664,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:53:00Z",
              "endTime": "2020-06-26T10:54:00Z",
            },
            "value": {
              "doubleValue": 14.467482387917698,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:52:00Z",
              "endTime": "2020-06-26T10:53:00Z",
            },
            "value": {
              "doubleValue": 14.445864404100575,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:51:00Z",
              "endTime": "2020-06-26T10:52:00Z",
            },
            "value": {
              "doubleValue": 14.385690295239328,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:50:00Z",
              "endTime": "2020-06-26T10:51:00Z",
            },
            "value": {
              "doubleValue": 14.510774863891129,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:49:00Z",
              "endTime": "2020-06-26T10:50:00Z",
            },
            "value": {
              "doubleValue": 14.667491664265981,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:48:00Z",
              "endTime": "2020-06-26T10:49:00Z",
            },
            "value": {
              "doubleValue": 14.614271363221633,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:47:00Z",
              "endTime": "2020-06-26T10:48:00Z",
            },
            "value": {
              "doubleValue": 15.133241074006946,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:46:00Z",
              "endTime": "2020-06-26T10:47:00Z",
            },
            "value": {
              "doubleValue": 14.481999476054625,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:45:00Z",
              "endTime": "2020-06-26T10:46:00Z",
            },
            "value": {
              "doubleValue": 14.531532624576357,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:44:00Z",
              "endTime": "2020-06-26T10:45:00Z",
            },
            "value": {
              "doubleValue": 14.666832340437395,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:43:00Z",
              "endTime": "2020-06-26T10:44:00Z",
            },
            "value": {
              "doubleValue": 15.094210209870653,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:42:00Z",
              "endTime": "2020-06-26T10:43:00Z",
            },
            "value": {
              "doubleValue": 14.840062739756831,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:41:00Z",
              "endTime": "2020-06-26T10:42:00Z",
            },
            "value": {
              "doubleValue": 14.93423863339558,
            },
          },
          {
            "interval": {
              "startTime": "2020-06-26T10:40:00Z",
              "endTime": "2020-06-26T10:41:00Z",
            },
            "value": {
              "doubleValue": 14.798206368868705,
            },
          },
        ],
      },
    ]};

  beforeAll(function() {
    d3.select("body")
        .append("svg")
        .attr("id", "chart")
        .attr("height", 400)
        .attr("width", 600);
  });

  afterEach(function() {
    d3.select("svg#chart").selectAll("*").remove();
  });

  it("should return an empty 2d list", function() {
    expect(formatPoints([])).toEqual([[], []]);
  });

  it("should return a nonempty 2d list", function() {
    expect(formatPoints(points)).toEqual(newPoints);
  });

  it("should make opacities 0 and show an error after drawing", function() {
    expect(d3.select("svg#chart")).not.toBeNull();

    d3.select("svg#chart")
        .append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "black")
        .attr("stroke-width", 1)
        .attr("d", d3.line()
            .y((d) => d[0])
            .x((d) => d[1]))
        .attr("opacity", 1)
        .attr("class", "timeSeries");
    expect(d3.select(".timeSeries")).not.toBeNull();
    expect(d3.select(".timeSeries").attr("opacity")).toEqual("1");
    showError("bad");
    expect(d3.select(".timeSeries").attr("opacity")).toEqual("0");
    expect(d3.select("#err")).not.toBeNull();
  });

  it("should draw chartData", async function() {
    const formattedResponse = new Response();
    formattedResponse.ok = true;
    formattedResponse.status = 200;
    formattedResponse.json = () => chartData;
    callFetch = jasmine.createSpy().and.returnValue(formattedResponse);

    await drawChart();
    expect(d3.select("#id0")).not.toBeNull();
    d3.selectAll(".timeSeries").each((elt, i) => {
      result = chartData["timeSeries"][i]["points"][0]["value"]["doubleValue"];
      expect(elt[0][0]).toEqual(result);
    });
  });

  it("should show an error due to an error in the response", async function() {
    const formattedResponse = new Response();
    formattedResponse.ok = false;
    formattedResponse.status = 100;
    callFetch = jasmine.createSpy().and.returnValue(formattedResponse);

    await drawChart();
    expect(d3.select("#err")).not.toBeNull();
  });
});
