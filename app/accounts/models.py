from datetime import datetime
# import hashlib
# from werkzeug.security import generate_password_hash, check_password_hash
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from markdown import markdown
# import bleach
# from flask import current_app, request, url_for
# from flask_login import UserMixin, AnonymousUserMixin
# from app.exceptions import ValidationError
from .. import db #, login_manager
from ..models import User


class Goal(db.Model):
    '''
    Model Class   :   Goal
    Description    :    Financial Goals of users linked to each Account and Transaction
    Added On       :    18/06/2017
    Updated On   :    18/06/2017
    Added By       :    Pradyumna Chatterjee(PC)
    Updated By   :    Pradyumna Chatterjee(PC)
    Reviewed On :   NA
    Reviewed By :   NA
    Future            :
                             * Add Model Methods
                             * Write Unit Tests
    Global Fields :
    Global Methods:
    '''
    __tablename__ = 'goals'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32)) # goal name
    goal_desc = db.Column(db.String(256))  # Nickname
    # TODO: VALIDATION - ENUM - Hobby/Travel/Marriage/ChildEd/Retirement
    goal_type = db.Column(db.String(16))
    goal_priority = db.Column(db.Integer)  # VALIDATION - 0 to 100

    comment_text = db.Column(db.String(128))
    added_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow)
    added_by = db.Column(db.String(16), default='System')
    updated_by = db.Column(db.String(16), default='System')


class AccountUser(User):
    '''
    Model Class   :   User
    Description    :    An extension of the Syetm user. Finance specific data will be included here
    Added On       :    18/06/2017
    Updated On   :    18/06/2017
    Added By       :    Pradyumna Chatterjee(PC)
    Updated By   :    Pradyumna Chatterjee(PC)
    Reviewed On :   NA
    Reviewed By :   NA
    Future            :
                             * Write Unit Tests
    Global Fields :
    Global Methods:
    '''
    __tablename__ = 'account_users'
    # id = db.Column(db.Integer, primary_key=True)
    pan_id_num = db.Column(db.String(16), unique=True)
    aadhar_id_num = db.Column(db.String(16), unique=True)  # PAN/Aadhar

    comment_text = db.Column(db.String(128))
    added_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow)
    added_by = db.Column(db.String(16), default='System')
    updated_by = db.Column(db.String(16), default='System')


class Account(db.Model):
    '''
    Model Class   :   Account
    Description    :    A generic account class for Savings/Wallets.
                                    For Fixed Income in(Non Market Linked) Instruments,
                                        Use Class AccountDetailsFixedIncome
                                    For Market Linked Instruments like Stock and Mutual Funds,
                                        Use Class AccountDetailsMarketLinkedIncome
    Added On       :    18/06/2017
    Updated On   :    18/06/2017
    Added By       :    Pradyumna Chatterjee(PC)
    Updated By   :    Pradyumna Chatterjee(PC)
    Reviewed On :   NA
    Reviewed By :   NA
    Future            :
                             * Add Model Methods
                             * Write Unit Tests
    Global Fields :
    Global Methods:
    '''
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    short_name = db.Column(db.String(16))  # Nickname
    long_name = db.Column(db.String(64))
    acc_num = db.Column(db.String(32))  # account Number/Folio ID/Dp+DEMAP ID
    # Savings/Current/TradingAcc/FD/RD/Special
    # RD/PPF/SmallSavings/Wallet/MF/Demat
    acc_type = db.Column(db.String(16))
    acc_bal = db.Column(db.DECIMAL)
    balance_on = db.Column(db.DateTime)  # stored proc/special function
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'))
    vendor = db.Column(db.String(32)) # company name
    # Branch name - web for online accounts
    vendor_branch = db.Column(db.String(32))

    # Property - Get Current Balance
    # Property - Set Current Balance


    comment_text = db.Column(db.String(128))
    added_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow)
    added_by = db.Column(db.String(16), default='System')
    updated_by = db.Column(db.String(16), default='System')


class AccountDetailsFixedIncome(Account):
    '''
    Model Class   :   AccountDetailsFixedIncome
    Description    :    An account class for all non market linked accounts
                                    * FD
                                    * RD
                                    * Small Savings (NSC/KVP/PO FD)
                                    * EPF
                                    * PPF
    Added On       :    18/06/2017
    Updated On   :    18/06/2017
    Added By       :    Pradyumna Chatterjee(PC)
    Updated By   :    Pradyumna Chatterjee(PC)
    Reviewed On :   NA
    Reviewed By :   NA
    Future            :
                             * Add Model Methods
                             * Write Unit Tests
    Global Fields :
    Global Methods:
    '''
    __tablename__ = 'account_details_fixed_income'
    id = db.Column(db.Integer, primary_key=True)
    acc_id = db.Column(db.Integer, db.ForeignKey('goals.id'))
    interest_rate_pa = db.Column(db.DECIMAL)
    # Daily, Weekly , Monthly, Quarterly, Halfyearly, Annually
    interest_freq = db.Column(db.String(16))
    interest_payout_type = db.Column(db.String(16))  # Payout/Compounding
    is_single_payment = db.Column(db.Boolean)
    maturity_bal = db.Column(db.DECIMAL)  # TODO: Should be a stored proc
    # TODO: Should be a stored proc - calculated
    current_bal = db.Column(db.DECIMAL)
    maturity_on = db.Column(db.DateTime)  # stored proc/special function

    # property - last transaction on
    # Property - Get Current Balance
    # Property - Set Current Balance

    comment_text = db.Column(db.String(128))
    added_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow)
    added_by = db.Column(db.String(16), default='System')
    updated_by = db.Column(db.String(16), default='System')


class AccountDetailsMarketLinkedIncome(Account):
    '''
    Model Class   :   AccountDetailsMarketLinkedIncome
    Description    :    An account class for all non market linked accounts
                                    * FD
                                    * RD
                                    * Small Savings (NSC/KVP/PO FD)
                                    * EPF
                                    * PPF
                                All sub accounts(like a folio's individual mfs or stocks)
                                    are listed in separate rows. EG
                                    * IOC :50
                                    * SBI :50
                                    * Reliance Liquid  Fund - Direct Plan : 47.2
    Added On       :    18/06/2017
    Updated On   :    18/06/2017
    Added By       :    Pradyumna Chatterjee(PC)
    Updated By   :    Pradyumna Chatterjee(PC)
    Reviewed On :   NA
    Reviewed By :   NA
    Future            :
                             * Add Model Methods
                             * Write Unit Tests
    Global Fields :
    Global Methods:
    '''
    __tablename__ = 'account_details_market_linked_income'
    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'))
    ticker_sym_id = db.Column(db.Integer, db.ForeignKey('market_unit.id'))
    unit_balance = db.Column(db.DECIMAL) # property or column?
    # Property - Last transaction on
    # Property - Get Current Balance
    # Property - Set Current Balance
    # Property - Get all unit balances for this account id
    # Property - Get total balances for this account id
    comment_text = db.Column(db.String(128))
    added_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow)
    added_by = db.Column(db.String(16), default='System')
    updated_by = db.Column(db.String(16), default='System')


class UserAccountsMapping(db.Model):
    '''
    Model Class   :   UserAccountsMapping
    Description    :   Maps a user to an account.
                                    Also records his/her share in the account

    Added On       :    18/06/2017
    Updated On   :    18/06/2017
    Added By       :    Pradyumna Chatterjee(PC)
    Updated By   :    Pradyumna Chatterjee(PC)
    Reviewed On :   NA
    Reviewed By :   NA
    Future            :
                             * Add Model Methods
                             * Write Unit Tests
                             * User share percentage to be dynamically
                                    updated through transactions
    Global Fields :
    Global Methods:
    '''
    __tablename__ = 'user_accounts_mappings'
    id = db.Column(db.Integer, primary_key=True)
    account_user_id = db.Column(db.Integer, db.ForeignKey('account_users.id'))
    acc_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    user_order = db.Column(db.Integer)  # 1/2/3
    # percentage of user's holdings in the account
    user_share = db.Column(db.DECIMAL)
    holding_mode = db.Column(db.String(8))  # Single/Joint, "E/S"

    comment_text = db.Column(db.String(128))
    added_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow)
    added_by = db.Column(db.String(16), default='System')
    updated_by = db.Column(db.String(16), default='System')


class MarketUnit(db.Model):
    '''
    Model Class   :   UserAccountsMapping
    Description    :   Curent and history value for all market linked units
                                    - One special unit to denote INR
                                    - TODO - To expand when using other currencies

    Added On       :    18/06/2017
    Updated On   :    18/06/2017
    Added By       :    Pradyumna Chatterjee(PC)
    Updated By   :    Pradyumna Chatterjee(PC)
    Reviewed On :   NA
    Reviewed By :   NA
    Future            :
                             * Add Model Methods
                             * Write Unit Tests
                             * Write python script to daily update:
                                    * MF data for all schemes in db
                                    * BSE/NSE data for all schemes in db
    Global Fields :
    Global Methods:
    '''
    __tablename__ = 'market_units'
    id = db.Column(db.Integer, primary_key=True)
    # actual symbol- IOC(NSE symbol), INR(currency), 113578(AMFI ID)
    urn = db.Column(db.String(16))
    # Todo: ENUM vaidation: "NSE symbol"/BSE Symbol/NASDAQ Symbol/AMFI ID/Currency
    urn_type = db.Column(db.String(16))
    unit_type = db.Column(db.String(8))  # Strock/MF
    unit_value = db.Column(db.DECIMAL)
    value_on = db.Column(db.DateTime) # diff from added_on
    active = db.Column(db.Boolean)  # only trhe latest element should be active
    #TODO: PROPERTY - unit_value in base currency terms
    # TODO: constraint - at any point only one urn should be present which is active
    # and is the latest one
    comment_text = db.Column(db.String(128))
    added_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime) # same as added_on
    added_by = db.Column(db.String(16), default='System')
    updated_by = db.Column(db.String(16), default='System')


class Transaction(db.Model):
    '''
    Model Class   :   Transaction
    Description    :   Holds all currency, mf and stock transaction insystem in single table
    Added On       :    18/06/2017
    Updated On   :    18/06/2017
    Added By       :    Pradyumna Chatterjee(PC)
    Updated By   :    Pradyumna Chatterjee(PC)
    Reviewed On :   NA
    Reviewed By :   NA
    Future            :
                             * Add Model Methods
                             * Write Unit Tests
                             * Write python script to daily update:
                                    * MF data for all schemes in db
                                    * BSE/NSE data for all schemes in db
    Global Fields :
    Global Methods:
    '''
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    acc_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    unit_count = db.Column(db.DECIMAL) #number of units transacted
    acc_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    ticker_sym_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    trans_dt = db.Column(db.DateTime, default=datetime.utcnow)
    trans_type = db.Column(db.String(2)) #dr/cr
    # TODO : Enum validation: scheduled/inprogress/completed/failed/reversed
    trans_status = db.Column(db.String(16))
    # TODO: PROPERTY - trans_value in base currency terms
    comment_text = db.Column(db.String(128))
    added_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow)
    added_by = db.Column(db.String(16), default='System')
    updated_by = db.Column(db.String(16), default='System')
