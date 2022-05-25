from typing import List
from colorama import Fore
import random

class Wordle:
	maxAttempts = 6
	def __init__(self,secret:str):
		self.secret:str=secret
		self.attemptlist=[]
		pass

	@property
	def solved(self):
		return len(self.attemptlist)>0 and self.attemptlist[-1] ==self.secret

	@property
	def remaining_att(self) ->int:
		return self.maxAttempts -len(self.attemptlist)

	@property
	def can_attempt(self):
		return self.remaining_att > 0 and not self.solved
	
	# @property
	# def attempt(self, word:str):
	# 	self.attemptlist.append(word)

	def guess(self,word:str):
		word=word.upper()
		result=[]

		for i in range(5):
			
			letter=LetterState(word[i])
			letter.is_in_word=word[i] in self.secret
			letter.is_in_position=word[i] == self.secret[i]
			result.append(letter)

		return result




class LetterState:
	def __init__(self,character:str):
		self.character:str=character
		self.is_in_word:bool = False
		self.is_in_position: bool = False

	def __repr__(self):
		return f"[{self.character} is_in_word:{self.is_in_word} is_in_position: {self.is_in_position}]"

def main():


	word_set=load_word_file("Allwords.txt")
	secret = random.choice(list(word_set))
	wordle=Wordle(secret)
	print("Welcome to the game")
	print(wordle)

	while wordle.can_attempt:
		word=input("\nEnter your word ....  ")
		word=word.upper()
		if len(word)!=5:
			print(Fore.RED+f"Word must be a 5 letter word"+Fore.RESET)
			continue
		if not word in word_set:
			print(Fore.RED+f"Word must be a 5 letter dictionary word"+Fore.RESET)
			continue
		wordle.attemptlist.append(word)
		result=wordle.guess(word)
		# print(*result,sep="\n")
		display_results(wordle)

	
	if wordle.solved:
		print(Fore.GREEN+f"You win!!"+Fore.RESET)
	else:
		print("Better luck next time")
		print("The word was ",wordle.secret)



def load_word_file(file_path:str):
	word_set=set()
	with open(file_path,"r") as f:
		for line in f.readlines():
			word=line.strip().upper()
			word_set.add(word)

	return word_set


def display_results(wordle: Wordle):
	lines=[]
	print("\n")
	for word in wordle.attemptlist:
		result=wordle.guess(word)
		colored_result=convert_to_color(result)
		lines.append(colored_result)
	
	for _ in range(wordle.remaining_att):
		lines.append(" ".join(["_"]*5))

	draw_boarder(lines)


def convert_to_color(result: List[LetterState]):
	result_with_color=[]
	for letter in result:
		if letter.is_in_position:
			color=Fore.GREEN
		elif letter.is_in_word:
			color=Fore.YELLOW
		else:
			color=Fore.WHITE
		colored_letter=color+letter.character+Fore.RESET
		result_with_color.append(colored_letter)

	return " ".join(result_with_color)  #will join the whole list into one string


def draw_boarder(lines:List[str],size:int=9,pad:int=1):
	content_length=size+pad*2
	top_boarder="┌"+"─"*content_length+"┐"
	bottom_boarder="╰"+"─"*content_length+"╯"
	space=" "*pad
	print(top_boarder)
	for line in lines:
		print("│"+space+line+space+"│")

	print(bottom_boarder)



if __name__=="__main__":
	main()