#This method shows a file with asciiArt, depends on the part in the game
import os
import random
import time
from functools import reduce
words=[]
playerErrors=0
totalPoints=0

def writeScore(score,name):
    scores=[]
    with open ("./utilities/highScores.txt","r",encoding="utf-8") as fr:
        for line in fr:
            scores.append(line.split("-"))    
        scores.append([score,name+"\n"])
        scores.sort(key=lambda score:int(score[0]),reverse=True)
    with open ("./utilities/highScores.txt","w+",encoding="utf-8") as fw:
        for idx,player in enumerate(scores):
            fw.write(str(player[0])+"-"+player[1])
    return scores

def showAsciiArt(fileName):
    with open ("./utilities/asciiArt/"+fileName+".txt","r",encoding="utf-8") as f:
        for line in f:
            print(line.rstrip())

#Load de dictionary of words for the game
def loadDictionary():
    with open ("./utilities/dictionary/data.txt","r",encoding="utf-8") as dic:
        for word in dic:
            words.append(word.rstrip())

#Return one new word to play
def selectNewWord():
    wordIndex=random.randint(0,len(words))
    wordGuess=words[random.randint(0,len(words))]
    words.pop(wordIndex)
    return wordGuess

def validateLetter(letter,rightWord,playerWord):
    global playerErrors
    letterIndex=-1
    indexWords=[idx for idx,val in enumerate(rightWord) if val==letter]

    if not indexWords:
        playerErrors=playerErrors+1
        letterIndex=-1
    else:
        letterIndex=1
        for idx in indexWords:
            playerWord[idx]=letter

    return letterIndex,playerWord


def run():
    global playerErrors,totalPoints
    answer=""
    rightWord=[]
    playerWord=[]
    playerLetters=[]
    flag=-1
    endGame=False
    playAgain=""
    playerName=input("Introduce yout nickname:")
    showAsciiArt("welcome")
      #Until the player press 'Y' the game will start
    while answer != "y":
        answer=input("""Are you ready to start the game?
                          Press 'y' when you ready """)
        if(answer=="y"):
            os.system("cls")
    loadDictionary()                          #Dictionary loading
    rightWord=selectNewWord()                 #Choose new word to play
    playerWord=['_' for letter in rightWord ] 
    showAsciiArt("begin")                     #Showing the first stage
    while(not endGame):
        print(playerWord)
        print(rightWord)
        print('\n')
        print("Score: "+str(totalPoints)+"\n")
        playerLetter=input("Please enter a letter: ")
                          #Validation to receive just 1 letter an non numeric character
        if(len(playerLetter)!=1 or playerLetter.isnumeric()):
            os.system("cls")
            print("Plese just entry a letter")
            continue
            
        if(playerLetter in playerLetters):
            os.system("cls")
            print("\nYou already used the letter: '"+playerLetter+"'. Try another letter.\n")
            continue    
        flag,playerWord=validateLetter(playerLetter,rightWord,playerWord)
        if(flag==-1):                    #The player made a mistake? show the next stage
            os.system("cls")
            showAsciiArt(str(playerErrors)+"Error")
            print("\nSORRY! The letter: '"+playerLetter+"' isn't in the word.\n")
            totalPoints-=(10,0)[totalPoints==0] 
        else:
            os.system("cls")
            print("¡Great Job!. The letter: '"+playerLetter+"' is in the word")
            totalPoints+=10        

        playerLetters.append(playerLetter)  #To save the letters that player already used
        if(rightWord==reduce(lambda a,b:a+b,playerWord)):       #The player win or lose?
            showAsciiArt("success")
            print("\nReady for the next word!. Your score is: "+str(totalPoints)+"\n")
            totalPoints+=100
            endGame=False
            rightWord=selectNewWord()
            playerWord=['_' for letter in rightWord ]
            playerErrors=0
            flag=-1
            playerLetters.clear()
            time.sleep(3)
            showAsciiArt("begin")
        elif(playerErrors==7):
            print("Your score was: "+str(totalPoints)+"\n")
            playAgain=input("Do you want to play again? y=yes any key=no")
            if(playAgain=="y"):
                endGame=False
                rightWord=selectNewWord()
                playerWord=['_' for letter in rightWord ]
                showAsciiArt("begin")
                playerErrors=0
                flag=-1
                playerLetters.clear()
            else:
                endGame=True
                print("Thanks for playing")
                print("Rank ---> Player- --> Score")
                for idx,player in enumerate(writeScore(totalPoints,playerName)):
                    print(str(idx+1)+"--->"+player[1].rstrip()+"--->"+str(player[0]))



if(__name__=="__main__"):
    run()



