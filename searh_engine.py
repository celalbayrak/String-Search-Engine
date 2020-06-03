# -*- coding: utf-8 -*-
"""
Created on Sat May  2 20:57:36 2020

@author: Celal
"""

import os

class TrieNode:  
    def __init__(self): 
        self.children = [None]*300
        self.isEndOfWord = False
        self.indexes=[]
        self.filenames=[]
        
class Trie: 
    def __init__(self): 
        self.root = self.getNode() 
  
    def getNode(self):  
        return TrieNode() 
  
    def charToIndex(self,ch): 
        if 48<=ord(ch) and 57>=ord(ch):
            return (ord(ch)-22)
        else:
            return (ord(ch)-ord('a'))
  
  
    def insert(self,key,word_index,file_name): 
        pCrawl = self.root 
        length = len(key) 
        for level in range(length): 
            index = self.charToIndex(key[level]) 
            if not pCrawl.children[index]: 
                pCrawl.children[index] = self.getNode() 
            pCrawl = pCrawl.children[index] 
        pCrawl.isEndOfWord = True
        pCrawl.indexes.append(word_index)
        pCrawl.filenames.append(file_name)
        pCrawl.filenames=list(set(pCrawl.filenames))
        
    def search(self, key): 
        arr=[]
        pCrawl = self.root 
        length = len(key) 
        for level in range(length): 
            index = self.charToIndex(key[level]) 
            if not pCrawl.children[index]: 
                return False
            pCrawl = pCrawl.children[index] #key found
        
        self.recursive(pCrawl,arr,key)    #searches under key


    def recursive(self,pCrawl,arr,key):
        chars=""
        if pCrawl is None:
            return
        if pCrawl.isEndOfWord:
            for i in arr:
                chars=chars+i
            print(key+chars)
            print("index: "+str(pCrawl.indexes))
            print("file name: " + str(pCrawl.filenames))
            print("-------------------------------------")
        for i in range(0,300):
            if pCrawl.children[i]:
                if i>=26:
                    char=chr(i+22)
                else:
                    char=chr(i+ord('a'))
                arr.append(char)
                self.recursive(pCrawl.children[i],arr,key)
                arr.pop()
    def recursive_common(self,pCrawl,arr,file_len):
        chars=""
        if pCrawl is None:
            return
        if pCrawl.isEndOfWord:
            if len(pCrawl.filenames)==file_len:
                for i in arr:
                    chars=chars+i
                print(chars)
        for i in range(0,300):
            if pCrawl.children[i]:
                if i>=26:
                    char=chr(i+22)
                else:
                    char=chr(i+ord('a'))
                arr.append(char)
                self.recursive_common(pCrawl.children[i],arr,file_len)
                arr.pop()
def read(path):
    f = open(path,"r")
    text=f.read()
    return text

def text_to_word(text):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    no_punct = ""
    for char in text:
       if char not in punctuations:
           no_punct = no_punct + char
       else:
           no_punct=no_punct+" "
    no_punct=no_punct.lower()
    words=no_punct.split()
    return words

def main():
    
    opt=input("If you want to find words and their indexes which are starting with given input, please enter 1. If you want to find common words, please enter 2: ")
    if opt=="1":
        path1=input("Please enter path:")
        if os.path.isdir(path1):
            files=os.listdir(path1)
            text_paths=[]
            
            for file in files:
                if file.endswith("txt"):
                    text_path=os.path.join(path1,file)
                    text_paths.append(text_path)
            while True:
                inpu=input("If you want to finish entering please type exit. Enter the prefix: ")
                inpu=inpu.lower()
                
                if inpu!="exit":
                    for text_file in text_paths:
                        word_index=0
                        text=read(text_file)
                        keys=text_to_word(text)
                        file_name=os.path.split(text_file)[1]
                        t = Trie() 
                        for key in keys:
                            t.insert(key,word_index,file_name)
                            word_index=word_index+len(key)
                        t.search(inpu)
                else:
                    break
        else:
            print("Directory does not exist")
    elif opt=="2":
        #path al
        path2=input("Please enter path:")
        if os.path.isdir(path2):
            files2=[]
            while True:
                inp=input("If you want to finish entering please type exit. Enter file name: ") 
                if inp != "exit": 
                    files2.append(inp)
                else:
                    break
                
            t = Trie() 
            word_index=0
            arr=[]
            text_paths2=[]
            for file in files2:
                if file.endswith("txt"):
                    text_path=os.path.join(path2,file)
                    text_paths2.append(text_path)
            for text_file in text_paths2:
                text=read(text_file)
                keys=text_to_word(text)
                file_name=os.path.split(text_file)[1]
                for key in keys:
                    t.insert(key,word_index,file_name)
                    word_index=word_index+len(key)
            t.recursive_common(t.root,arr,len(text_paths2))
        else:
            print("Directory does not exist")
    else:
        print("Invalid input")
if __name__ == '__main__': 
    main() 