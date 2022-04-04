// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;

contract SimpleStorage {
    uint256 number;
    struct People {
        uint256 number;
        string name;
    }
    // People public person = People({
    //     number:2,
    //     name:"elias"
    // });
    People[] public people;
    mapping(string => uint256) public nameToNumber;

    function store(uint256 _number) public {
        number = _number;
        // return number;
    }

    function addPerson(uint256 _number, string memory _name) public {
        people.push(People({number: _number, name: _name}));
        nameToNumber[_name] = _number;
    }

    function retrieve() public view returns (uint256) {
        return number;
    }
}
