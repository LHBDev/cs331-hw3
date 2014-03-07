#!/usr/bin/env python3

import sys, itertools, time

#Global Vars
hotelList = []
sortedHotels = []
bidList = []
lBids = []
sBids = []
currMaxWeight = 0
bids = 0
hotels = 0

class Hotels:
	''' Build the list of Hotels and reserves '''
	def __init__(self, q, reserve, hotelID, bidID = -1):
		self.q = q
		self.reserve = reserve
		self.hotelID = hotelID
		self.bidID = bidID

class Bids:
	''' Build the list of Bids and their properties '''
	def __init__(self, bType, amount, target, bidID):
		self.bType = bType
		self.amount = amount
		self.target = target
		self.bidID = bidID

def readNumHotels(inputfile):
	return int(inputfile.readline())

def readHotels(inputfile, x):
	y = (inputfile.readline()).split()
	z = Hotels(int(y[0]), int(y[1]), x)
	hotelList.append(z)
	sortedHotels.append(z)

def dummyBids():
	global currMaxWeight
	for item in hotelList:
		amount = item.reserve
		currMaxWeight += amount
		bType = 1
		target = hotelList.index(item)
		bidID = -1
		bid = Bids(bType, amount, target, bidID)
		sBids[item.hotelID] = bid 

def printStuff():
	print (currMaxWeight, end=" ")
	for hotel in hotelList:
		print(hotel.bidID, end=" ")
	print()

def flatBids(bid):
	global bids, currMaxWeight
	bType = int(bid[0])
	amount = int(bid[1])
	target = int(bid[2])
	bidID = bids
	bids +=1
	sbid = Bids(bType, amount, target, bidID)
	bidList.append(sbid)

	#check if beats reserve or previous bid
	hotel = hotelList[sbid.target]
	if(sbid.amount > hotel.reserve):
		oldbid = sBids[hotel.hotelID]
		if ( oldbid.bType == 2):
			#handle replacing linear bid
			sBids[hotel.hotelID] = sbid
			currMaxWeight -= hotel.reserve
			hotel.reserve = sbid.amount
			hotel.bidID = sbid.bidID
			currMaxWeight += sbid.amount
			shift(oldbid, sBids.index(sbid))
		else:
			sBids[hotel.hotelID] = sbid
			hotel.reserve = sbid.amount
			hotel.bidID = sbid.bidID
			currMaxWeight -= oldbid.amount
			currMaxWeight += sbid.amount

def shift(bid, idx):
	global currMaxWeight
	while(idx < hotels and not(sBids[idx] == None)):
		oldbid = lBids[idx]
		lBids[idx] = bid
		bid = oldbid
		hotel = hotelList[idx]
		currMaxWeight -= hotel.reserve
		amount = bid.target * hotel.q + bid.amount
		currMaxWeight += amount
		hotel.reserve = amount
		hotel.bidID = bid.bidID
		if(not(sBids[idx] == None)):
			sBids[idx] = None
			break;
		idx += 1

def linearBids(bid):
	global bids, currMaxWeight
	bType = int(bid[0])
	amount = int(bid[1])
	target = int(bid[2])
	bidID = bids
	bids += 1
	lbid = Bids(bType, amount, target, bidID)
	bidList.append(lbid)

	for hotel in sortedHotels:
		amount = (lbid.target * hotel.q) + lbid.amount
		if(amount > hotel.reserve):
			oldbid = bidList[hotel.bidID]
			currMaxWeight -= hotel.reserve
			hotel.bidID = lbid.bidID
			hotel.reserve = amount
			currMaxWeight += amount
			if(oldbid.bType == 2):
				lBids[sortedHotels.index(hotel)] = lbid
				shift(oldbid, lBids.index(lbid))
			else:
				sBids[hotel.hotelID] = None
			break
			

def readbids(line):
	global bids
	y = line.split()
	if( int(y[0]) == 1):
		flatBids(y)
	elif (int(y[0]) == 2):
		linearBids(y)
	elif (int(y[0]) == 3):
		printStuff()

def main():
	global hotels, lBids, sBids
	inputFileName = sys.argv[1]
	inputfile = open(inputFileName, "r")

	#read number of hotels
	hotels = readNumHotels(inputfile)
	for x in range(hotels):
		sBids.append(None)
		lBids.append(None)
	#read in all hotels
	for x in range(hotels):
		readHotels(inputfile, x)
	sortedHotels.sort(key=lambda x: x.q, reverse=True)

	dummyBids()
	start = time.clock()

	for line in inputfile:
		readbids(line)
	elapsed = time.clock() - start
	print (elapsed)


if __name__ == '__main__':
	main()