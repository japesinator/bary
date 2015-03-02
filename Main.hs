-- Code by JP Smith, HackIllinois 2015
--
-- Its name is Bary
module Main where

import Control.Monad
import Data.Char
import Data.List
import System.IO

type Board = [String]

flipBoard :: Board -> Board
flipBoard = map $ map swap where
  swap '@' = 'O'
  swap 'O' = '@'
  swap a   = a

parseBoard :: String -> Board
parseBoard = chunks 8 . takeWhile (`elem` "-|O@") . dropWhile (`notElem` "-|O@")

parseMoves :: String -> [(Int,Int)]
parseMoves [] = []
parseMoves l@(f:_) = case f of
                          'T' -> map (\[a,b] -> (a,b))
                               $ chunks 2
                               $ map digitToInt
                               $ filter (`elem` "1234567890") l
                          'R' -> tail
                               $ map (\[a,b] -> (a,b))
                               $ chunks 2
                               $ map digitToInt
                               $ filter (`elem` "1234567890") l
                          _   -> []

chunks :: Int -> [a] -> [[a]]
chunks _ [] = []
chunks n l = take n l : chunks n (drop n l)

flips :: (Int, Int) -> Board -> Int
flips c b = sum $ map (($ b) . ($ c)) [hflips, vflips]

replaceAt :: Int -> a -> [a] -> [a]
replaceAt n x xs = take n xs ++ [x] ++ drop (n + 1) xs

hflips :: (Int, Int) -> Board -> Int
hflips (x,y) b = rowFlips $ replaceAt x '*' (b !! y)

rowFlips :: String -> Int
rowFlips [] = 0
rowFlips (x : xs) = case x of
                         '*' -> tilAt 0 xs
                         '@' -> tilStar 0 xs
                         _   -> rowFlips xs
  where
    tilAt _ [] = 0
    tilAt n (y : ys) = case y of
                            'O' -> tilAt (n + 1) ys
                            '@' -> n
                            _   -> 0
    tilStar _ [] = 0
    tilStar n (y : ys) = case y of
                              'O' -> tilStar (n + 1) ys
                              '*' -> n + rowFlips ys
                              _   -> rowFlips $ dropWhile (/= '*') ys

vflips :: (Int, Int) -> Board -> Int
vflips c = hflips c . transpose

main :: IO ()
main = do hFlush stdout
          begin <- getLine
          let color = case last begin of
                            '@' -> "Black"
                            'O' -> "White"
                            _   -> "Grey"
          putStrLn "A"
          hFlush stdout
          forever (do hFlush stdout
                      status <- getLine
                      let moves = parseMoves status
                      let board = (if color == "White"
                                 then flipBoard
                                 else id) $ parseBoard status
                      let move = case moves of
                                      [] -> (7,7)
                                      l  -> fst
                                          $ foldl1 (\x y -> if snd x > snd y then x else y)
                                          $ map (\c -> (c, flips c board)) l
                      putStrLn $ (\(a,b) -> show a ++ "," ++ show b) move
                      hFlush stdout
                  )
