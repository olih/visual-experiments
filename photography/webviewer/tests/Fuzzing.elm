module Fuzzing exposing(oneOfList, exGroupInfo, mediaFileInfo, defaultMediaFile)
import Fuzz as Fuzz exposing (Fuzzer, list, string)
import MediaFileInfo
import Set
oneOfList: List a -> Fuzzer a
oneOfList list =
    List.map Fuzz.constant list |> Fuzz.oneOf

exGroupInfo: String
exGroupInfo = """
{
  "tags": [
    "London",
    "2017",
    "2018"
  ],
  "items": [
    {
      "item": "image1.jpg",
      "folder": "folder1",
      "tags": [
        "2018",
        "London"
      ]
    },
    {
      "item": "image2.jpg",
      "folder": "folder1",
      "tags": [
        "2017",
        "London"
      ]
    },
    {
      "item": "image3.jpg",
      "folder": "folder3",
      "tags": [
        "2017",
        "Paris"
      ]
    },
    {
      "item": "image4.jpg",
      "folder": "folder3",
      "tags": [
      ]
    }
    ]
}
"""

createMediaFileInfo: (String, List String) -> MediaFileInfo.Model
createMediaFileInfo twoParams =
    MediaFileInfo.Model (Tuple.first twoParams) (Tuple.first twoParams) (Set.fromList (Tuple.second twoParams))

mediaFileInfo: Fuzzer MediaFileInfo.Model
mediaFileInfo = Fuzz.tuple (string, list string) |> Fuzz.map createMediaFileInfo

defaultMediaFile: MediaFileInfo.Model
defaultMediaFile =
    createMediaFileInfo ("default", ["tag"])