module Test.Generated.Main1791660962 exposing (main)

import MediaItemUnitTests
import MultiContentUnitTests
import RangeParamsUnitTests

import Test.Reporter.Reporter exposing (Report(..))
import Console.Text exposing (UseColor(..))
import Test.Runner.Node
import Test

main : Test.Runner.Node.TestProgram
main =
    [     Test.describe "MediaItemUnitTests" [MediaItemUnitTests.suite],     Test.describe "MultiContentUnitTests" [MultiContentUnitTests.suite],     Test.describe "RangeParamsUnitTests" [RangeParamsUnitTests.suite] ]
        |> Test.concat
        |> Test.Runner.Node.run { runs = Nothing, report = (ConsoleReport UseColor), seed = 264831844615231, processes = 4, paths = ["/Users/olivier/Documents/github/visual-experiments/brush-ui/tests/Fuzzing.elm","/Users/olivier/Documents/github/visual-experiments/brush-ui/tests/MediaItemUnitTests.elm","/Users/olivier/Documents/github/visual-experiments/brush-ui/tests/MultiContentUnitTests.elm","/Users/olivier/Documents/github/visual-experiments/brush-ui/tests/RangeParamsUnitTests.elm"]}