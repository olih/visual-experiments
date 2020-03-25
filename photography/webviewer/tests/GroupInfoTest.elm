module GroupInfoTest exposing (..)

import Expect exposing (Expectation)
import Fuzz exposing (Fuzzer, int, list, string)
import Test exposing (..)
import Fuzzing as Fuzzing
import GroupInfo as GroupInfo
import Json.Decode exposing (decodeString)

expected = { item = "image1.jpg"
    , folder = "folder1"
    , tags = ["2018","London"]
    }

suite : Test
suite =
    describe "MediaFileInfo Module"
    [
     describe "toString"
        [
            test "decode a json group info payload" <|
                \_ ->
                    decodeString GroupInfo.decoder Fuzzing.exGroupInfo
                    |> Result.toMaybe 
                    |> Maybe.map .items
                    |> Maybe.withDefault []
                    |> List.head
                    |> Expect.equal (Just expected)
       ]

    ]