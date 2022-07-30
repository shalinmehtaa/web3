// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage {
    // this will get initialized to 0!
    uint256 favoriteNumber; // unsigned integer; meaning neither positive nor negative

    // bool favoriteBool = true;
    // string favoriteString = "String";
    // int256 favoriteInt = -5;
    // address favoriteAddress = 0xeEE32c44e011b58AE745eDaE1bD91828C00AaEAb;
    // bytes32 favoriteBytes = "cat"; //the string can be converted to a bytes object

    struct People {
        uint256 favoriteNumber;
        string name;
    }

    // complex types
    People[] public people;
    mapping(string => uint256) public nameToFavoriteNumber;

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    // view allows us to read from the blockchain (no need for tx as we are not changing state)
    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    // pure functions can do some operation without writing to the blockchain (no change of state)

    // memory = will only be stored during the execution of the function
    // storage = will be stored on the blockchain
    function addPerson(uint256 _favoriteNumber, string memory _name) public {
        people.push(People(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}
