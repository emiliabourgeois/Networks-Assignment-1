import requests
import sys
import random

user_id = random.randrange(1,10000)

url = "http://" + str(sys.argv[1]) + ":" + str(sys.argv[2]) + "/" + str(user_id) + "/"

def print_menu():
    print("   User ID: " + str(user_id))
    print("1. Make play");
    print("2. Check result");
    print("3. Check score");
    print("4. Reset");
    print("5. Exit");
        
def make_play():
    valid_input = False;
    options = ('R', 'P', 'S');
     
    while(valid_input == False):
        client_input = input("Enter R for rock, P for paper or S for scissors\n").upper();
        
        if client_input in options:
            valid_input = True;
            
    tmp = url + client_input

    r = requests.post(tmp);
    print(r.text)
    return client_input;
    
def check_result():
    tmp = url + "result"
    status = requests.get(tmp);   
    print(status.text);
    
def check_score():
    status = requests.get('smoreurl/scorefile');

def reset():
    valid_input = False;
    options = ('Y', 'N');

    while(valid_input == False):
        client_input = input("Reset score? Y/N: ").upper()
        
        if client_input in options:
            valid_input = True
            tmp = url + "reset"
            r = requests.post(tmp);
            print(r.text)
            
def main():
    loop = True
    while (loop): 
        print_menu();
        choice = int(input("Select game option: "));
        
        
        if choice == 1:
            make_play()
            
        elif choice == 2:
            check_result()
            
        elif choice == 3:
            check_score()
        
        elif choice == 4:
            reset()
            
        elif choice == 5:
            print("Goodbye");
            loop = False
            
        else:
            input("Invalid selection, press any key to try again")

main()