
from VeriFlow.Network import Network

ROUTE_VIEW = 1;
BIT_BUCKET = 2;


def main():
	print("Enter network configuration file name (eg.: file.txt):");
	filename = input("> ");
	# filename = "Topo1.txt"
	network = Network();
	network.parseNetworkFromFile(filename);
	generatedECs = network.getECsFromTrie();
	network.checkWellformedness();
	network.log(generatedECs);


	#the task of finding maximum network visibility
	# for now, assume the cost of choose each switch is 1
	# construct a dict to store the visibility of each switch

	all_sws = list(network.switches.keys())
	print("All switches: ", all_sws)
	visibility = {}
	for sw in all_sws:	# sw is the IP address of the switch
		visibility[sw] = network.switches.get(sw).getNextHops()	# getNextHops() returns a list of switch IPs

	while True:
		print("Enter the number of switches you want to choose: ")
		num = int(input("> "))
		cnt = 0
		not_chosen = all_sws.copy()
		max_vis_sws = []
		while cnt < num:
			if len(max_vis_sws) == len(all_sws):
				break
			#get the switch with the maximum visibility from not_chosen
			max_sw = max(not_chosen, key=lambda x: len(visibility[x]))
			not_chosen.remove(max_sw)
			for sw in visibility[max_sw]:
				if sw not in max_vis_sws:
					max_vis_sws.append(sw)
			cnt += 1
		# get the chosen switches
		chosen = [item for item in all_sws if item not in not_chosen]
		print("The chosen switches are: ")
		for i in chosen:
			print(i)
		print("The switches that can be reached from the chosen switches are: ")
		for i in max_vis_sws:
			print(i)
		print("with visibility: ", len(max_vis_sws))
	


	





	# # the task of checking what other nodes a switch can reach and on what classes of IP addresses
	# # print switch list
	# print("Switches: ");
	# for switch in network.switches:
	# 	print(switch);
	# # print EC list
	# print("ECs: ");
	# for ec in generatedECs:
	# 	print(ec.toString());
	# # print tree
	# # print("Trie: ")
	# # network.getTrie().printTrie(network.getTrie().getRoot(), "")
	# # let user choose a switch, determine what other switches it can reach and on what classes of IP addresses
	# while True:
	# 	print("Enter switch IP: ");
	# 	switchIP = input("> ");
	# 	print("Switch can reach:")
	# 	for rule in network.switches[switchIP].getRules():
	# 		nextHop = network.switches[rule.getNextHopId()]
	# 		# print(rule.getPrefix())
	# 		EC_from_rule = network.getTrie().getECfromRule(rule.getPrefix(), None, "")
	# 		print("Next hop: " + nextHop.getId(), end=" ")
	# 		print(" on EC: " , end=" ")
	# 		for ec in EC_from_rule:
	# 			print(ec.toString(), end=" ")
	# 		print(" ")

			



	# while True:
	# 	print(" ");
	# 	print("Add rule by entering A#switchIP-rulePrefix-nextHopIP (eg.A#127.0.0.1-128.0.0.0/2-127.0.0.2)");
	# 	print("Remove rule by entering R#switchIP-rulePrefix-nextHopIP (eg.R#127.0.0.1-128.0.0.0/2-127.0.0.2)");
	# 	print("To exit type exit");

	# 	affectedEcs = set()
	# 	inputline = input('> ')
	# 	if (inputline.startswith("A")):
	# 		affectedEcs = network.addRuleFromString(inputline[2:]);
	# 		network.checkWellformedness(affectedEcs);
	# 	elif (inputline.startswith("R")):
	# 		affectedEcs = network.deleteRuleFromString(inputline[2:]);
	# 		network.checkWellformedness(affectedEcs);
	# 	elif ("exit" in inputline):
	# 		break;
	# 	else:
	# 		print("Wrong input format!");
	# 		continue;

	# 	print("");
	# 	network.log(affectedEcs);

if __name__ == '__main__':
	main()