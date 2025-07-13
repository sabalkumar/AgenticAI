from datetime import datetime


def get_share_price(symbol: str) -> float:
    """Returns current price for given stock symbol"""
    prices = {
        'AAPL': 150.0,
        'TSLA': 250.0,
        'GOOGL': 120.0
    }
    return prices.get(symbol.upper(), 0.0)


class Account:
    def __init__(self, account_id: str, initial_deposit: float) -> None:
        """Initialize a new account with given ID and initial deposit"""
        if initial_deposit < 0:
            raise ValueError("Initial deposit cannot be negative")
            
        self.account_id = account_id
        self.balance = initial_deposit
        self.initial_deposit = initial_deposit
        self.holdings = {}
        self.transactions = []
        
        # Record initial deposit transaction
        self._record_transaction('DEPOSIT', {'amount': initial_deposit})
    
    def _record_transaction(self, transaction_type: str, details: dict) -> None:
        """Internal method to record transaction details"""
        transaction = {
            'timestamp': datetime.now(),
            'type': transaction_type,
            'details': details,
            'balance': self.balance
        }
        self.transactions.append(transaction)
    
    def deposit(self, amount: float) -> bool:
        """Add funds to the account balance"""
        if amount <= 0:
            return False
            
        self.balance += amount
        self._record_transaction('DEPOSIT', {'amount': amount})
        return True
    
    def withdraw(self, amount: float) -> bool:
        """Remove funds from the account if sufficient balance exists"""
        if amount <= 0:
            return False
            
        if self.balance < amount:
            return False
            
        self.balance -= amount
        self._record_transaction('WITHDRAWAL', {'amount': amount})
        return True
    
    def buy_shares(self, symbol: str, quantity: int) -> bool:
        """Purchase shares if sufficient funds are available"""
        if quantity <= 0:
            return False
            
        price = get_share_price(symbol)
        if price == 0.0:
            return False  # Unknown symbol
            
        total_cost = price * quantity
        
        if self.balance < total_cost:
            return False
            
        self.balance -= total_cost
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        
        self._record_transaction('BUY', {
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'total_cost': total_cost
        })
        
        return True
    
    def sell_shares(self, symbol: str, quantity: int) -> bool:
        """Sell shares if sufficient quantity is owned"""
        if quantity <= 0:
            return False
            
        current_quantity = self.holdings.get(symbol, 0)
        if current_quantity < quantity:
            return False
            
        price = get_share_price(symbol)
        if price == 0.0:
            return False  # Unknown symbol
            
        total_value = price * quantity
        
        self.balance += total_value
        self.holdings[symbol] -= quantity
        
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        
        self._record_transaction('SELL', {
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'total_value': total_value
        })
        
        return True
    
    def get_portfolio_value(self) -> float:
        """Calculates total portfolio value (cash + stock value)"""
        stock_value = 0.0
        
        for symbol, quantity in self.holdings.items():
            price = get_share_price(symbol)
            stock_value += price * quantity
            
        return self.balance + stock_value
    
    def get_profit_loss(self) -> float:
        """Calculates current profit/loss from initial deposit"""
        return self.get_portfolio_value() - self.initial_deposit
    
    def get_holdings(self) -> dict:
        """Returns dictionary of current stock holdings {symbol: quantity}"""
        return self.holdings.copy()
    
    def get_transaction_history(self) -> list:
        """Returns list of all transactions in chronological order"""
        return self.transactions.copy()
    
    def get_balance(self) -> float:
        """Returns current cash balance"""
        return self.balance