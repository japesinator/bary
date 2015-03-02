# The MIT License (MIT)
# 
# Copyright (c) 2015 Allston Trading, LLC
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
# ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH
# THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys


def log(message):
    sys.stderr.write(str(message) + "\n")
    sys.stderr.flush()


def send(message):
    print message
    sys.stdout.flush()
    log("SENT: " + message)


def parseBoard(boardStr):
    row = 0
    board = []
    board.append([])

    for square in boardStr:
        if square == '|':
            row = row + 1
            board.append([])
        else:
            board[row].append(square)


def parseMoves(messageArray, start):
    moves = []
    for i in range(start, len(messageArray)):
        moves.append([])
        moveStrs = messageArray[i].split(',');
        moves[i - start].append(int(moveStrs[0]))
        moves[i - start].append(int(moveStrs[1]))
    return moves


def makeMove(board, moves):
    # creative things should happen here
    send(str(moves[0][0]) + "," + str(moves[0][1]))


def main():
    READY = 'A'

    RESPOND_TURN = 'R'
    BEGIN = 'B'
    TURN = 'T'
    SKIPPED = 'S'
    log('here')

    while 1:
        line = raw_input()
        log("GOT: " + line)
        tokens = line.split(' ')
        messageType = tokens[0]
        if messageType == BEGIN:
            send(READY)
        elif messageType == TURN:
            board = parseBoard(tokens[1])
            moves = parseMoves(tokens, 2)
            makeMove(board, moves)
        elif messageType == RESPOND_TURN:
            board = parseBoard(tokens[1])
            lastMove = tokens[2].split(',')
            moves = parseMoves(tokens, 3)
            makeMove(board, moves)
        elif messageType == SKIPPED:
            log("SKIPPED")
        else:
            send('?' + messageType)


if __name__ == "__main__":
    main()



