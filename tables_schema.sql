
Create Table Vehicles(
	VehicleNo varchar(12),
	Brand varchar(25),
	Model varchar(12),
	primary key(VehicleNo)
);

Create Table Services(
	ServiceID int identity(1,1),
	ServiceType varchar(10),
	VehicleNo varchar(12) FOREIGN KEY REFERENCES Vehicles(VehicleNo),
	Primary key(ServiceID),
);
