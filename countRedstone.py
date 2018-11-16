#
#CATEGORIES:
#Basic Components: Pistons, redstone dust, redstone torches, repeaters, comparators, redstone blocks, observer blocks
#Containers: Dispenser, Dropper, trapped chest, hoppers
#Doors, Fence gates, Trapdoors: All wooden and iron doors, all fence gates, wooden & iron trapdoors
#Sources(non-redstone): Lever, stone & wooden buttons, all pressure plates, tripwire hooks, string, daylight sensors
#Rails: detector rail, powered rail, activator rail
#Misc: Note block, TNT, redstone lamps, Slime blocks
#Slimestone: Pistons, Redstone block, Slime block, observer block
#Carts: Minecart with chest, hopper and furnace
#Filter by Ed0
#v1.5
#Any bug or idea contact me via https://twitter.com/el_Ed0_
#

import mcplatform
from albow.dialogs import Dialog
from albow import TableView, TableColumn, Button, Widget, Column
from pymclevel.materials import alphaMaterials
from time import gmtime, strftime

displayName = "Count Redstone Components"

#49 components total
basic = (29, 33, 55, 75, 76, 93, 94, 149, 150, 152, 218)
containers = (23, 146, 154, 158)
doors = (64, 71, 96, 107, 167, 183, 184, 185, 186, 187, 193, 194, 195, 196, 197)
sources = (69, 70, 72, 77, 131, 132, 143, 147, 148, 151, 178)
rails = (27, 28, 157)
misc = (25, 46, 123, 124, 165)
slimestone = (29, 33, 152, 165, 218)
carts = ('MinecartChest', 'MinecartHopper', 'MinecartFurnace')

subtypes = False
filepath = ""

inputs = (
	("Basic components", True),
	("Containers", False),
	("Doors, Fence gates, Trapdoors", False),
	("Power Sources(non-redstone)", False),
	("Rails", False),
	("Misc", False),
	("Slimestone", False),
	("Carts", False),
	("Show subtypes",False),
	("File name (date if empty):",("string","value=None")),
)
def idtoname(x):
    return {
		23: "Dispenser",
		25: "Note block",
		27: "Powered rail",
		28: "Detector rail",
		29: "Sticky Piston",
		33: "Piston",
		46: "TNT",
		55: "Redstone dust",
		64: "Door",
		69: "Lever",
		70: "Stone Pressure plate",
		71: "Iron Door",
		72: "Wood Pressure plate",
		75: "Redstone torch",
		76: "Redstone torch",
		77: "Stone Button",
		93: "Redstone Repeater",
		94: "Redstone Repeater",
		96: "Trapdoor",
		107: "Fence gate",
		123: "Redstone lamp",
		124: "Redstone lamp",
		131: "Tripwire hook",
		132: "Tripwire",
		143: "Wooden Button",
		146: "Trapped chest",
		147: "Golden Pressure plate",
		148: "Iron Pressure plate",
		149: "Comparator",
		150: "Comparator",
		151: "Daylight sensor",
		152: "Redstone Block",
		154: "Hopper",
		157: "Activator rail",
		158: "Dropper",
		165: "Slime Block",
		167: "Iron Trapdoor",
		178: "Daylight sensor",
		183: "Fence gate",
		184: "Fence gate",
		185: "Fence gate",
		186: "Fence gate",
		187: "Fence gate",
		193: "Door",
		194: "Door",
		195: "Door",
		196: "Door",
		197: "Door",
		218: "Observer block",
		'MinecartChest': "Minecart Chest",
		'MinecartHopper': "Minecart Hopper",
		'MinecartFurnace': "Minecart Furnace",
    }[x]

def costinrd(x):
#id 27, 28 & 157 r
	return{
		23: 1,
		25: 1,
		27: 1,
		28: 1,
		29: 1,
		33: 1,
		55: 1,
		75: 1,
		76: 1,
		93: 3,
		94: 3,
		123: 4,
		124: 4,
		149: 3,
		150: 3,
		152: 9,
		157: 1,
		158: 1,
		218: 2,
	}.get(x, 0)	
		
def perform(level, box, options):
	global subtypes
	subtypes = options["Show subtypes"]
	global filepath
	filepath = options["File name (date if empty):"]
	basicb = options["Basic components"]
	containersb = options["Containers"]
	doorsb = options["Doors, Fence gates, Trapdoors"]
	sourcesb = options["Power Sources(non-redstone)"]
	railsb = options["Rails"]
	miscb = options["Misc"]
	slimestoneb = options["Slimestone"]
	cartsb = options["Carts"]
	
	print 'starting scanning...'
	total = {}
	
	#Components
	for x in xrange(box.minx, box.maxx):
		for z in xrange(box.minz, box.maxz):	
			for y in xrange(box.miny, box.maxy):
				block = level.blockAt(x,y,z)
				if(block == 0):
					continue
				
				
				if((basicb and block in basic) or (containersb and block in containers) or (doorsb and block in doors) or
					(sourcesb and block in sources) or (railsb and block in rails) or (miscb and block in misc) or
					(slimestoneb and block in slimestone)):
					if subtypes:
						identifier = block
						data = level.blockDataAt(x,y,z)
					else:
						identifier = idtoname(block)
						data = block
					if not identifier in total:
						total[ identifier ] = {}
					if not data in total[ identifier ]:
						total[ identifier ][ data ] = 0
					total[ identifier ][ data ]+=1
	
	#Entities
	if cartsb:
		for (chunk, slices, point) in level.getChunkSlices(box):
			for e in chunk.Entities:
				x = e["Pos"][0].value
				y = e["Pos"][1].value
				z = e["Pos"][2].value

				if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz:
					id = e["id"].value
				
					if id in carts:
						identifier = idtoname(id)
						data = id
					if not identifier in total:
						total[ identifier ] = {}
					if not data in total[ identifier ]:
						total[ identifier ][ data ] = 0
					total[ identifier ][ data ]+=1
	
	
	
	print 'finished scanning'
	tableview = TableView(columns=[TableColumn("Block",400),TableColumn("Count",70),
	TableColumn("Stack",70),TableColumn("Items",70),TableColumn("Price in dust",70)])
	
	res = []
	text = "Block; Count; Stacks; items; Price;\n"
	totalPrice = 0
	
	if subtypes:
		for (block, v) in total.iteritems():
			for (data, count) in v.iteritems():
				price = 0
				if block in rails:
					#add 1 to price cause python rounds down. 5/6 returns 0 but 5 rails cost 1 dust
					price = costinrd(block)*(count/6)
					price +=1
				else:
					price = costinrd(block)*count
				totalPrice+=price
				res.append( [" - " + alphaMaterials[block, data].name, str(count), str(count/64), str(count-((count/64)*64)), str(price)] )
				text+=str(str(alphaMaterials[block, data].name)+"; "+str(count)+"; "+str(count/64)+"; "+str(count-((count/64)*64))+"; "+str(price)+";\n")
	else:
		for (name, v) in total.iteritems():
			price = 0
			realCount = 0
			for (id, count) in v.iteritems():
				if id in rails:
					price+=(costinrd(id)*(count/6))
					price+=1
				else:
					price+=(costinrd(id)*count)
				realCount+=count
			if (str(name) == "Door") or (str(name) == "Iron Door"):
				count/=2
			totalPrice+=price
			res.append( [" - " + str(name), str(realCount), str(realCount/64), str(realCount-((realCount/64)*64)), str(price)] )
			text+=str(str(name)+"; "+str(realCount)+"; "+str(realCount/64)+"; "+str(realCount-((realCount/64)*64))+"; "+str(price)+";\n")
		
	res.append( [" - TOTAL COST IN DUST ", str(totalPrice), str(totalPrice/64), str(totalPrice-((totalPrice/64)*64)), "-"] )
	text+=str("TOTAL COST IN DUST; "+str(totalPrice)+"; "+str(totalPrice/64)+"; "+str(totalPrice-((totalPrice/64)*64))+"; "+"-;\n")
		
	tableview.num_rows = lambda: len(res)
	tableview.row_data = lambda i: (res[i][0], res[i][1], res[i][2], res[i][3], res[i][4])
		
	tableview.shrink_wrap()
	
	widget = Widget()
	widget.add(tableview)
	widget.shrink_wrap()
	
	def save():
		if filepath == "None":
			print 'filepath is empty'
			file = open(level.displayName +"_"+ strftime("%Y.%m.%d %H.%M.%S", gmtime())+".txt","w")
			file.writelines(str(text))
			file.close()
		else:
			file = open(filepath ,"w")
			file.writelines(str(text))
			file.close()

	log = Button("Log to file", action=save)
	col = Column((widget, log))
	Dialog(client=col, responses=["OK"]).present()