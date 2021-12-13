# Import necessary packages
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

# Pass the connection string to a variable, conn_url
conn_url = 'postgresql://postgres:123@localhost/GroupProject'

# Create an engine that connects to PostgreSQL server
engine = create_engine(conn_url)

# Establish a connection
connection = engine.connect()

# Pass the SQL statements that create all tables
stmt = """
CREATE TABLE basic_info (
	Id int,
	LotArea int,
	tot_room_num int,
	SalePrice int,
	primary key (id)
);

CREATE TABLE sales_info (
	sales_id int references basic_info (Id),
	SalePrice int,
	MoSold smallint,
	YrSold int,
	SaleType varchar (5),
	SaleCondition varchar (10),
	primary key (sales_id)
);

CREATE TABLE rooms (
	room_id int references basic_info (Id),
	tot_room_num int, 
	bathroom_num int,
	bedroom_num int,
	kitchen_num int,
	basement_num int,
    garage_num int,
	primary key (room_id)
);

CREATE TABLE garage (
	garage_id int references rooms (room_id),
	garage_num int,
	GarageType varchar (8),
	GarageYrBlt int,
	GarageFinish varchar (3),
	GarageCars smallint,
	GarageArea int,
	GarageQual char (2),
	GarageCond char (2),
	primary key (garage_id)
);

CREATE TABLE basement (
	basement_id int references rooms (room_id),
	basement_num int,
	BsmtQual varchar(5),
	BsmtCond varchar(5),
	BsmtExposure varchar (5),
	BsmtFinType1 varchar (5),
	BsmtFinSF1 smallint,
	BsmtFinType2 varchar(5),
	BsmtFinSF2 int,
	BsmtUnfSF int,
	TotalBsmtSF int,
	primary key (basement_id)
);

CREATE TABLE bathroom (
	bathroom_id int references rooms (room_id),
	bathroom_num int,
	BsmtFullBath smallint,
	BsmtHalfBath smallint,
	FullBath smallint,
	HalfBath smallint,
	primary key (bathroom_id)
);

CREATE TABLE kitchen (
	kitchen_id int references rooms (room_id),
	kitchen_num int,
	kitchenQual varchar(5),
	primary key (kitchen_id)
);

CREATE TABLE amenities (
	property int references basic_info (Id),
	pool_num int,
	tot_porch_size int,
	fireplace_num int,
	primary key (property)
);

CREATE TABLE fireplace (
	fireplace_id int references amenities (property),
	fireplace_num smallint,
	FireplaceQu char (2),
	primary key (fireplace_id)
);

CREATE TABLE porch (
	porch_id int references amenities (property),
	tot_porch_size int,
	OpenPorchSF int,
	EnclosedPorch int,
	thrSsnPorch int,
	ScreenPorch int,
	primary key (porch_id)
);

CREATE TABLE pool (
	pool_id int references amenities (property),
	pool_num int,
	PoolArea int,
	PoolQC char (2),
	primary key (pool_id)
);

CREATE TABLE msinformation (
	Id int references basic_info (Id),
	MSSubClass varchar(100),
	MSZoning varchar(100),
	primary key (Id)
);

CREATE TABLE quality_and_condition (
	Id int references basic_info (Id),
	OverallQual varchar(100),
	OverallCond varchar(100),
	YearBuilt int,
	YearRemodAdd int,
	primary key (Id)
);

CREATE TABLE electricity (
	Id int references basic_info (Id),
	Heating varchar(5),
	HeatingQC varchar(5),
	CentralAir varchar(5),
	Electrical varchar(10),
	primary key (Id)
);

CREATE TABLE neighborhood_info(
	neighborhood_id int references basic_info (Id),
	Neighborhood varchar(100),
	Condition1 varchar(100),
	Condition2 varchar(100),
	primary key (neighborhood_id)
);

CREATE TABLE dwelling (
	dwelling_id int references basic_info (Id),
	BldgType varchar(100),
	HouseStyle varchar(100),
	primary key (dwelling_id)
);
"""

# Execute the statement to create tables
connection.execute(stmt)


# Create tables in Python

data = pd.read_csv('train.csv')

basic_info = data[['Id','LotArea', 'TotRmsAbvGrd', 'SalePrice']]
basic_info = basic_info.rename(columns = {'TotRmsAbvGrd':'tot_room_num'})
basic_info.columns = basic_info.columns.str.lower()
basic_info = basic_info.set_index('id')

sales_info = data[["Id","SalePrice","MoSold","YrSold","SaleType","SaleCondition"]]
sales_info = sales_info.rename(columns = {'Id':'sales_id'})
sales_info.columns = sales_info.columns.str.lower()
sales_info = sales_info.set_index('sales_id')

bathroom = data[['Id', 'BsmtFullBath', 'BsmtHalfBath', 'FullBath', 'HalfBath']]
bathroom['bathroom_num'] = data['BsmtFullBath'] + data['BsmtHalfBath'] + data['FullBath'] + data['HalfBath']
bathroom = bathroom.rename(columns = {'Id':'bathroom_id'})
bathroom = bathroom[['bathroom_id', 'bathroom_num', 'BsmtFullBath', 'BsmtHalfBath', 'FullBath', 'HalfBath']]
bathroom.columns = bathroom.columns.str.lower()
bathroom = bathroom.set_index('bathroom_id')

porch = data[['Id', 'OpenPorchSF', 'EnclosedPorch', '3SsnPorch', 'ScreenPorch']]
porch['tot_porch_size'] = porch['OpenPorchSF'] + porch['EnclosedPorch'] + porch['3SsnPorch'] + porch['ScreenPorch']
porch = porch[['Id', 'tot_porch_size', 'OpenPorchSF', 'EnclosedPorch', '3SsnPorch', 'ScreenPorch']]
porch = porch.rename(columns = {'Id':'porch_id', '3SsnPorch':'thrssnporch'})
porch.columns = porch.columns.str.lower()
porch = porch.set_index('porch_id')

kitchen = data[['Id', 'KitchenAbvGr', 'KitchenQual']]
kitchen = kitchen.rename (columns = {'Id':'kitchen_id', 'KitchenAbvGr':'kitchen_num'})
kitchen.columns = kitchen.columns.str.lower()
kitchen = kitchen.set_index('kitchen_id')

fireplace = data[['Id', 'Fireplaces', 'FireplaceQu']]
fireplace = fireplace.rename (columns = {'Id':'fireplace_id', 'Fireplaces':'fireplace_num'})
fireplace.columns = fireplace.columns.str.lower()
fireplace = fireplace.set_index('fireplace_id')

msinformation = data [['Id','MSSubClass','MSZoning']]
msinformation.columns = msinformation.columns.str.lower()
msinformation = msinformation.set_index('id')

quality_and_condition = data[['Id', 'OverallQual', 'OverallCond', 'YearBuilt', 'YearRemodAdd']]
quality_and_condition.columns = quality_and_condition.columns.str.lower()
quality_and_condition = quality_and_condition.set_index('id')

electricity = data[['Id', 'Heating','HeatingQC', 'CentralAir', 'Electrical']]
electricity.columns = electricity.columns.str.lower()
electricity = electricity.set_index('id')

neighborhood_info = data[['Id', 'Neighborhood','Condition1','Condition2']]
neighborhood_info = neighborhood_info.rename(columns = {'Id':'neighborhood_id'})
neighborhood_info.columns = neighborhood_info.columns.str.lower()
neighborhood_info = neighborhood_info.set_index('neighborhood_id')

dwelling = data[['Id','BldgType','HouseStyle']]
dwelling = dwelling.rename(columns = {'Id':'dwelling_id'})
dwelling.columns = dwelling.columns.str.lower()
dwelling = dwelling.set_index('dwelling_id')


garage = data[['Id', 'GarageType', 'GarageYrBlt', 'GarageFinish', 'GarageCars', 'GarageArea', 'GarageQual','GarageCond']]
garage['garage_num'] = garage['GarageType'].where(garage['GarageType'].notnull(),0)
garage['garage_num'] = garage['GarageType'].where(garage['GarageType'].isnull(),1)
garage["garage_num"].fillna(0, inplace = True)
garage = garage.rename(columns = {'Id':'garage_id'})
garage.columns = garage.columns.str.lower()
garage = garage.set_index('garage_id')

pool = data[['Id','PoolArea','PoolQC']]
pool = pool.rename(columns = {'Id':'pool_id'})
pool['pool_num'] = pool['PoolQC'].where(pool['PoolQC'].notnull(),0)
pool['pool_num'] = pool['PoolQC'].where(pool['PoolQC'].isnull(),1)
pool['pool_num'].fillna(0, inplace = True)
pool.columns = pool.columns.str.lower()
pool = pool.set_index('pool_id')

basement = data[['Id', 'BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinSF1', 'BsmtFinType2', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF']]
basement = basement.rename(columns = {'Id':'basement_id'})
basement['basement_num'] = basement['BsmtQual'].where(basement['BsmtQual'].notnull(),0)
basement['basement_num'] = basement['BsmtQual'].where(basement['BsmtQual'].isnull(),1)
basement['basement_num'].fillna(0, inplace = True)
basement = basement[['basement_id', 'basement_num', 'BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinSF1', 'BsmtFinType2', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF']]
basement.columns = basement.columns.str.lower()
basement = basement.set_index('basement_id')

amenities = pd.DataFrame()
amenities['pool_num'] = pool['pool_num']
amenities['tot_porch_size'] = porch['tot_porch_size']
amenities['fireplace_num'] = fireplace['fireplace_num']
amenities.index.names = ['property']

rooms = data[['Id', 'TotRmsAbvGrd', 'BedroomAbvGr']]
rooms = rooms.rename(columns = {'Id':'room_id', 'TotRmsAbvGrd':'tot_room_num', 'BedroomAbvGr':'bedroom_num'})
rooms = rooms.merge(bathroom, how='left', left_on='room_id', right_on='bathroom_id')
rooms = rooms.merge(kitchen, how='left', left_on='room_id', right_on='kitchen_id')
rooms = rooms.merge(basement, how='left', left_on='room_id', right_on='basement_id')
rooms = rooms.merge(garage, how='left', left_on='room_id', right_on='garage_id')
rooms = rooms[['room_id', 'tot_room_num', 'bathroom_num', 'bedroom_num', 'kitchen_num', 'basement_num', 'garage_num']]
rooms = rooms.set_index('room_id')

# Write tables to pgAdmin
basic_info.to_sql('basic_info', engine, if_exists='append')
sales_info.to_sql('sales_info', engine, if_exists='append')
rooms.to_sql('rooms', engine, if_exists='append')
garage.to_sql('garage', engine, if_exists='append')
basement.to_sql('basement', engine, if_exists='append')
bathroom.to_sql('bathroom', engine, if_exists='append')
kitchen.to_sql('kitchen', engine, if_exists='append')
amenities.to_sql('amenities', engine, if_exists='append')
fireplace.to_sql('fireplace', engine, if_exists='append')
porch.to_sql('porch', engine, if_exists='append')
pool.to_sql('pool', engine, if_exists='append')
msinformation.to_sql('msinformation', engine, if_exists='append')
quality_and_condition.to_sql('quality_and_condition', engine, if_exists='append')
electricity.to_sql('electricity', engine, if_exists='append')
neighborhood_info.to_sql('neighborhood_info', engine, if_exists='append')
dwelling.to_sql('dwelling', engine, if_exists='append')

#close the connection
connection.close()