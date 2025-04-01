# Projet_TPOOO
import random
import json
import os

class BankSystem:
    def __init__(self, users_file="users.txt"):
        self.users_file = users_file
        self.load_users()

    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, "r") as file:
                self.users = json.load(file)
        else:
            self.users = {}

    def save_users(self):
        with open(self.users_file, "w") as file:
            json.dump(self.users, file, indent=4)

    def generate_card_number(self):
        return str(random.randint(10**15, 10**16 - 1))

    def create_user(self, name, address, phone, cnic, login, password, daily_limit):
        user_id = str(len(self.users) + 1)
        if cnic in [user["cnic"] for user in self.users.values()]:
            print("CNIC déjà enregistré.")
            return
        
        account_type = "Épargne" if daily_limit < 50000 else "Courant"
        card_number = self.generate_card_number()
        pin = input("Entrez votre code PIN (4 chiffres) : ")
        
        self.users[user_id] = {
            "name": name,
            "address": address,
            "phone": phone,
            "cnic": cnic,
            "login": login,
            "password": password,
            "balance": 0,
            "daily_limit": daily_limit,
            "account_type": account_type,
            "card_number": card_number,
            "pin": pin,
            "transactions": []
        }
        self.save_users()
        print(f"Compte créé avec succès ! Votre numéro de carte : {card_number}")
    
    def deposit(self, user_id, amount):
        if user_id in self.users:
            self.users[user_id]["balance"] += amount
            self.users[user_id]["transactions"].append(f"Dépôt de {amount}")
            self.save_users()
            print(f"Dépôt réussi ! Nouveau solde : {self.users[user_id]['balance']}")
        else:
            print("Utilisateur introuvable.")
    
    def withdraw(self, user_id, amount):
        user = self.users.get(user_id)
        if not user:
            print("Utilisateur introuvable.")
            return
        
        if amount > user["balance"]:
            print("Fonds insuffisants.")
            return
        
        if amount > user["daily_limit"]:
            print("Montant excède la limite quotidienne.")
            return
        
        user["balance"] -= amount
        user["transactions"].append(f"Retrait de {amount}")
        self.save_users()
        print(f"Retrait réussi ! Nouveau solde : {user['balance']}")
    
    def check_balance(self, user_id):
        user = self.users.get(user_id)
        if user:
            print(f"Solde actuel : {user['balance']}")
        else:
            print("Utilisateur introuvable.")
    
    def transfer(self, sender_id, receiver_id, amount):
        sender = self.users.get(sender_id)
        receiver = self.users.get(receiver_id)
        
        if not sender or not receiver:
            print("Un des utilisateurs est introuvable.")
            return
        
        if amount > sender["balance"]:
            print("Fonds insuffisants.")
            return
        
        sender["balance"] -= amount
        receiver["balance"] += amount
        sender["transactions"].append(f"Transfert de {amount} à {receiver['name']}")
        receiver["transactions"].append(f"Réception de {amount} de {sender['name']}")
        self.save_users()
        print(f"Transfert réussi ! Nouveau solde : {sender['balance']}")
    
    def transaction_history(self, user_id):
        user = self.users.get(user_id)
        if user:
            print("Historique des transactions :")
            for t in user["transactions"]:
                print(t)
        else:
            print("Utilisateur introuvable.")


# Exemple d'utilisation
def main():
    bank = BankSystem()
    while True:
        print("\n1. Créer un compte\n2. Déposer\n3. Retirer\n4. Vérifier solde\n5. Transférer\n6. Historique des transactions\n7. Quitter")
        choice = input("Choisissez une option : ")
        
        if choice == "1":
            name = input("Nom complet : ")
            address = input("Adresse : ")
            phone = input("Téléphone : ")
            cnic = input("CNIC : ")
            login = input("Login : ")
            password = input("Mot de passe : ")
            daily_limit = float(input("Limite quotidienne de retrait : "))
            bank.create_user(name, address, phone, cnic, login, password, daily_limit)
        elif choice == "2":
            user_id = input("ID utilisateur : ")
            amount = float(input("Montant à déposer : "))
            bank.deposit(user_id, amount)
        elif choice == "3":
            user_id = input("ID utilisateur : ")
            amount = float(input("Montant à retirer : "))
            bank.withdraw(user_id, amount)
        elif choice == "4":
            user_id = input("ID utilisateur : ")
            bank.check_balance(user_id)
        elif choice == "5":
            sender_id = input("ID expéditeur : ")
            receiver_id = input("ID destinataire : ")
            amount = float(input("Montant à transférer : "))
            bank.transfer(sender_id, receiver_id, amount)
        elif choice == "6":
            user_id = input("ID utilisateur : ")
            bank.transaction_history(user_id)
        elif choice == "7":
            break
        else:
            print("Option invalide.")

if __name__ == "__main__":
    main()
