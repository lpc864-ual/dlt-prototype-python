import hashlib
import json
import time
import random
from datetime import datetime


class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        """
        Inicializa un bloque en la blockchain.
        
        Args:
            index (int): Posición del bloque en la cadena
            previous_hash (str): Hash del bloque anterior
            timestamp (float): Marca de tiempo cuando se crea el bloque
            data (dict/list/str): Datos a almacenar en el bloque
            nonce (int): Número usado una vez para la prueba de trabajo
        """
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()
        
    def calculate_hash(self):
        """
        Calcula el hash del bloque usando SHA-256.
        
        Returns:
            str: Hash hexadecimal del bloque
        """
        # Convertimos el bloque a string y calculamos su hash
        block_string = json.dumps({
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "data": self.data,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        
        return hashlib.sha256(block_string).hexdigest()
    
    def __str__(self):
        """Representación en string del bloque para facilitar visualización"""
        return (
            f"Block #{self.index}\n"
            f"Hash: {self.hash}\n"
            f"Previous Hash: {self.previous_hash}\n"
            f"Timestamp: {datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Data: {self.data}\n"
            f"Nonce: {self.nonce}\n"
        )


class Blockchain:
    def __init__(self, difficulty=3):
        """
        Inicializa la cadena de bloques.
        
        Args:
            difficulty (int): Número de ceros iniciales requeridos para el hash
        """
        self.chain = []
        self.difficulty = difficulty
        self.pending_transactions = []
        
        # Crear el bloque génesis
        self.create_genesis_block()
        
    def create_genesis_block(self):
        """
        Crea el primer bloque de la cadena (bloque génesis).
        """
        genesis_block = Block(0, "0", time.time(), {"message": "Bloque Génesis"})
        self.mine_block(genesis_block)
        self.chain.append(genesis_block)
        
    def get_latest_block(self):
        """
        Obtiene el último bloque en la cadena.
        
        Returns:
            Block: El último bloque añadido a la cadena
        """
        return self.chain[-1]
    
    def mine_block(self, block):
        """
        Realiza la prueba de trabajo para encontrar un hash válido.
        
        Args:
            block (Block): Bloque a minar
            
        Returns:
            Block: Bloque con un hash válido que cumple con la dificultad
        """
        # Un hash válido debe comenzar con 'difficulty' número de ceros
        target = "0" * self.difficulty
        
        # Primero realizamos el proceso de "lotería"
        # Simulamos un proceso aleatorio antes de intentar encontrar el hash
        # lottery_value = self.perform_lottery()
        # block.data["lottery_result"] = lottery_value
        
        print(f"Minando bloque {block.index}...")
        start_time = time.time()
        
        # Ahora buscamos un hash válido (con 3 ceros iniciales)
        while block.hash[:self.difficulty] != target:
            block.nonce += 1
            block.hash = block.calculate_hash()
            
            # Cada 100000 intentos mostramos progreso
            if block.nonce % 100000 == 0:
                print(f"Intentos: {block.nonce}, Hash actual: {block.hash}")
        
        mining_time = time.time() - start_time
        print(f"¡Bloque minado! Hash: {block.hash}")
        print(f"Nonce encontrado: {block.nonce}")
        print(f"Tiempo de minado: {mining_time:.2f} segundos")
        
        # Verificar si además hemos conseguido el "hash de 13"
        # if self.is_special_hash(block.hash):
            # print("¡Felicidades! Has encontrado un hash especial (hash de 13)")
            # block.data["special_hash"] = True
        
        return block
    
    # def perform_lottery(self):
        """
        Simula un proceso de lotería antes de buscar el hash.
        Esto representa el concepto mencionado de "primero lotería y luego conseguir el hash".
        
        Returns:
            int: Resultado de la lotería
        """
        print("Realizando proceso de lotería...")
        # Simulamos un proceso aleatorio
        lottery_result = random.randint(1, 1000)
        print(f"Resultado de la lotería: {lottery_result}")
        return lottery_result
    
    
    # def is_special_hash(self, hash_string):
        """
        Verifica si el hash cumple la condición especial (hash de 13).
        En este caso, interpretamos "hash de 13" como un hash que contiene "13" en alguna parte.
        
        Args:
            hash_string (str): El hash a verificar
            
        Returns:
            bool: True si es un hash especial, False en caso contrario
        """
        return "13" in hash_string
    
    def is_valid_new_block(self, new_block, previous_block):
        """
        Verifica si un nuevo bloque es válido.
        
        Args:
            new_block (Block): Bloque a validar
            previous_block (Block): Bloque anterior en la cadena
            
        Returns:
            bool: True si el bloque es válido, False en caso contrario
        """
        # Verificar si el índice es correcto
        if previous_block.index + 1 != new_block.index:
            print("Índice inválido")
            return False
            
        # Verificar si el hash del bloque anterior coincide
        if previous_block.hash != new_block.previous_hash:
            print("Hash anterior inválido")
            return False
            
        # Verificar si el hash del bloque es válido
        if new_block.calculate_hash() != new_block.hash:
            print("Hash del bloque inválido")
            return False
            
        # Verificar si el hash cumple con la dificultad
        if new_block.hash[:self.difficulty] != "0" * self.difficulty:
            print("La prueba de trabajo no cumple con la dificultad requerida")
            return False
            
        return True
    
    def add_transaction(self, transaction):
        """
        Añade una transacción pendiente que se incluirá en el próximo bloque.
        
        Args:
            transaction (dict): Datos de la transacción
        """
        # Añadir timestamp a la transacción
        transaction['timestamp'] = time.time()
        self.pending_transactions.append(transaction)
        print(f"Transacción añadida al pool: {transaction}")
    
    def append_block(self, data=None):
        """
        Operación 'append': Crea y añade un nuevo bloque a la cadena.
        Esta es la operación fundamental en una blockchain.
        
        Args:
            data (dict, optional): Datos a incluir en el bloque. 
                                  Si es None, se usan las transacciones pendientes.
        
        Returns:
            Block: El nuevo bloque añadido a la cadena
        """
        if data is None:
            # Si no se proporcionan datos, usamos las transacciones pendientes
            data = {'transactions': self.pending_transactions.copy()}
            # Limpiamos las transacciones pendientes
            self.pending_transactions = []
        
        latest_block = self.get_latest_block()
        new_block = Block(
            index=latest_block.index + 1,
            previous_hash=latest_block.hash,
            timestamp=time.time(),
            data=data
        )
        
        # Minar el bloque (encontrar un hash válido)
        self.mine_block(new_block)
        
        # Verificar que el bloque es válido antes de añadirlo
        if self.is_valid_new_block(new_block, latest_block):
            self.chain.append(new_block)
            print(f"Bloque #{new_block.index} añadido a la cadena")
            return new_block
        else:
            print("Error: El bloque no es válido, no se añadió a la cadena")
            return None
    
    def is_chain_valid(self):
        """
        Verifica que toda la cadena de bloques es válida.
        
        Returns:
            bool: True si la cadena es válida, False en caso contrario
        """
        for i in range(1, len(self.chain)):
            previous_block = self.chain[i-1]
            current_block = self.chain[i]
            
            # Verificar vínculo con el bloque anterior
            if current_block.previous_hash != previous_block.hash:
                print(f"Referencia de hash anterior inválida en el bloque {i}")
                return False

            # Verificar hash actual
            if current_block.hash != current_block.calculate_hash():
                print(f"Hash inválido en el bloque {i}")
                return False
                
            # Verificar prueba de trabajo
            if current_block.hash[:self.difficulty] != "0" * self.difficulty:
                print(f"Prueba de trabajo inválida en el bloque {i}")
                return False
                
        return True
    
    def print_chain(self):
        """
        Imprime todos los bloques de la cadena de manera legible.
        """
        print("\n=== BLOCKCHAIN ===")
        for block in self.chain:
            print(block)
            print("-" * 30)


# Demostración del funcionamiento de la blockchain
def run_demo():
    # Crear una blockchain con dificultad de 3 (3 ceros al inicio del hash)
    my_blockchain = Blockchain(difficulty=3)
    
    print("\n=== Blockchain inicializada con bloque génesis ===")
    my_blockchain.print_chain()
    
    # Añadir algunas transacciones
    my_blockchain.add_transaction({"from": "Alice", "to": "Bob", "amount": 10})
    my_blockchain.add_transaction({"from": "Bob", "to": "Charlie", "amount": 5})
    
    # Crear un nuevo bloque con las transacciones pendientes
    print("\n=== Añadiendo bloque con transacciones ===")
    my_blockchain.append_block()
    my_blockchain.print_chain()
    
    # Añadir otro bloque con un mensaje directo
    print("\n=== Añadiendo bloque con mensaje directo ===")
    my_blockchain.append_block({"message": "Bloque con datos directos"})
    my_blockchain.print_chain()
    
    # Verificar la validez de la cadena
    print("\n=== Verificando la validez de la cadena ===")
    is_valid = my_blockchain.is_chain_valid()
    print(f"¿La blockchain es válida? {'Sí' if is_valid else 'No'}")


if __name__ == "__main__":
    run_demo()