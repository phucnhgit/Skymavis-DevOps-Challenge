instance = {
    "1": "us-west-a", 
    "2": "us-west-b", 
    "3": "us-west-c"
    }
subnets = {
    "1": "us-west-a", 
    "2": "us-west-b", 
    "3": "us-west-b", 
    "4": "us-west-c",
    "5": "us-west-a", 
    "6": "us-west-b", 
    "7": "us-west-b", 
    "8": "us-west-c",
    "9": "us-west-a", 
    "10": "us-west-b", 
    "11": "us-west-b", 
    "12": "us-west-c",
    "13": "us-west-a", 
    "14": "us-west-b", 
    "15": "us-west-b", 
    "16": "us-west-c",
    }

def func_allocated(instance, subnets):
    nat = list(instance.values())
    subnet = list(subnets.values())

    count_nat = {key: nat.count(key) for key in nat}
    count_sn = {key: subnet.count(key) for key in subnet}

    max_sn = round(len(subnet)/len(nat))
    allocated = [[]*max_sn]*len(nat)
    # Allocate Subnet in the same NAT GW:
    for idx in range(0, len(nat)):
        if (nat[idx] in count_sn):
            # Number of subnets allocated
            n_alloc_subnet = int(count_sn[nat[idx]] / count_nat[nat[idx]])
            # Assign subnet to nat gw
            allocated[idx] = ([nat[idx] for items in range(0, n_alloc_subnet)])
            # Subtract total subnet
            count_sn[nat[idx]] -= n_alloc_subnet
            count_nat[nat[idx]] -= 1
            # Delete subnet when all was allocated
            if (count_sn[nat[idx]] == 0):
                # Filter subnet was allocated
                del count_sn[nat[idx]]
                subnet = list(filter(lambda x: (x != nat[idx]), subnet))

    # Allocate remain subnnets
    for idx in range(0, len(nat)):
        if (len(allocated[idx]) < max_sn):
            n_alloc_subnet = max_sn - len(allocated[idx])
            if (n_alloc_subnet > len(subnet)):
                n_alloc_subnet = len(subnet)
            allocated[idx] += (subnet[0:n_alloc_subnet])
            subnet = subnet[n_alloc_subnet:]
            if (len(subnet) == 0):
                break

    if (len(subnet) > 0):
        allocated[0] += subnet[0:]

    return allocated

def print_result(allocated):
    nat_key = list(instance.keys())
    nat_values = list(instance.values())
    subnets_key = list(subnets.keys())
    subnets_values = list(subnets.values())

    for idx in range(0, len(nat_values)):
        print("\033[1;32m Instance (%s - %s):" % (nat_key[idx],nat_values[idx]))
        for sb in allocated[idx]:
            sb_idx = subnets_values.index(sb)
            print("\033[1;30m   subnet (%s - %s)" % (subnets_key[sb_idx], sb))
            del subnets_key[sb_idx]
            del subnets_values[sb_idx]

        

if __name__ == "__main__":
    allocated = func_allocated(instance, subnets)
    print_result(allocated)