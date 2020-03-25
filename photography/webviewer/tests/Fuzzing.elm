module Fuzzing exposing(oneOfList, exGroupInfo)
import Fuzz exposing (Fuzzer, int, list, string)


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

