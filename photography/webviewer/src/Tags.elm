module Tags exposing (toTags, reset)

import Set exposing (Set)
import Json.Decode as Decode exposing (Decoder, list, string)
toSetDecoder : Decoder (List comparable) -> Decoder (Set comparable)
toSetDecoder listDecoder =
    Decode.map Set.fromList listDecoder

toTags: Decoder (Set String)
toTags =
    list string |> toSetDecoder

reset: Set String
reset =
    Set.empty