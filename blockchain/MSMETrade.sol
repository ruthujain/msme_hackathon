pragma solidity ^0.8.0;

contract MSMETrade {

    address public owner;

    mapping(uint => Shipment) public shipments;

    struct Shipment {
        uint id;
        string product;
        string hsnCode;
        bool delivered;
        bool paid;
    }

    event ShipmentCreated(uint shipmentId, string product, string hsnCode);
    event PaymentReleased(uint shipmentId);

    constructor() {
        owner = msg.sender;
    }

    function createShipment(uint shipmentId, string memory product, string memory hsnCode) public {
        require(msg.sender == owner, "Only the owner can create a shipment");
        shipments[shipmentId] = Shipment(shipmentId, product, hsnCode, false, false);
        emit ShipmentCreated(shipmentId, product, hsnCode);
    }

    function markDelivered(uint shipmentId) public {
        require(msg.sender == owner, "Only the owner can mark the shipment as delivered");
        shipments[shipmentId].delivered = true;
    }

    function releasePayment(uint shipmentId) public {
        require(shipments[shipmentId].delivered, "Shipment must be delivered first");
        require(!shipments[shipmentId].paid, "Payment already released");
        shipments[shipmentId].paid = true;
        emit PaymentReleased(shipmentId);
    }

    function deposit(uint amount) public payable {
        require(msg.value == amount, "Incorrect deposit amount");
    }
}
