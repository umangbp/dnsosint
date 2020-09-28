import re
import argparse
import validators
import sys
import dnsdumpster


print("""

      :::::::::  ::::    :::  :::::::: 
     :+:    :+: :+:+:   :+: :+:    :+: 
    +:+    +:+ :+:+:+  +:+ +:+         
   +#+    +:+ +#+ +:+ +#+ +#++:++#++   
  +#+    +#+ +#+  +#+#+#        +#+    
 #+#    #+# #+#   #+#+# #+#    #+#     
#########  ###    ####  ########       
      ::::::::   :::::::: ::::::::::: ::::    ::: ::::::::::: 
    :+:    :+: :+:    :+:    :+:     :+:+:   :+:     :+:      
   +:+    +:+ +:+           +:+     :+:+:+  +:+     +:+       
  +#+    +:+ +#++:++#++    +#+     +#+ +:+ +#+     +#+        
 +#+    +#+        +#+    +#+     +#+  +#+#+#     +#+         
#+#    #+# #+#    #+#    #+#     #+#   #+#+#     #+#          
########   ######## ########### ###    ####     ###     

------------------------------------------------------------------------------
                            By - Umang Patel
------------------------------------------------------------------------------

""")

def main():

    # creating object of argument parser
    parser = argparse.ArgumentParser()

	# add optional and required arguments that user can enter
    parser.add_argument("domain", help='Domain to scan')
    
    # list of arguments parsed by user
    arguments = parser.parse_args()

    # check if domain provided by user is correct or not
    # if not correct exit the app
    if validators.domain(arguments.domain):
        target_domain = arguments.domain
    else:
        print("Invalid Domain Supplied")
        sys.exit()

    print()

    # making request to dns dumpster
    dnsdumpster.getDnsDumpster(target_domain)

# invoking main function
if __name__ == '__main__':

	main()