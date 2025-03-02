// ParkingSpot.java
class ParkingSpot {
    private boolean occupied;
    
    public ParkingSpot() {
        this.occupied = false;
    }

    public boolean isOccupied() {
        return occupied;
    }

    public void park() {
        this.occupied = true;
    }

    public void leave() {
        this.occupied = false;
    }
}

// ParkingLot.java
class ParkingLot {
    private ParkingSpot[] spots;

    public ParkingLot(int size) {
        this.spots = new ParkingSpot[size]; // Bug: Does not initialize each ParkingSpot object
    }

    public void parkCar(int spotIndex) {
        ParkingSpot spot = spots[spotIndex]; // NullPointerException occurs here
        if (!spot.isOccupied()) {
            spot.park();
            System.out.println("Car parked at spot " + spotIndex);
        } else {
            System.out.println("Spot " + spotIndex + " is already occupied.");
        }
    }
}

// Main.java
public class Main {
    public static void main(String[] args) {
        ParkingLot lot = new ParkingLot(5);
        lot.parkCar(0); // This will cause a NullPointerException
    }
}
