const { ethers } = require("hardhat")
const { expect, assert } = require("chai")
const { FallbackProvider } = require("@ethersproject/providers")

describe("SimpleStorage", function () {
    let simpleStorageFactory, simpleStorage
    beforeEach(async function () {
        simpleStorageFactory = await ethers.getContractFactory("SimpleStorage")
        simpleStorage = await simpleStorageFactory.deploy()
    })

    it("Should start with a favourite number of 0", async function () {
        const currentValue = await simpleStorage.favouriteNumber()
        const expectedValue = "0"
        assert.equal(currentValue.toString(), expectedValue)
        // expect(currentValue.toString()).to.equal(expectedValue)
    })

    it("Should update when we call store", async function () {
        const expectedValue = "17"
        const updateTransaction = await simpleStorage.store(expectedValue)
        await updateTransaction.wait(1)
        const updatedValue = await simpleStorage.favouriteNumber()
        assert.equal(updatedValue.toString(), expectedValue)
    })

    it("Should return the contents of the people array", async function () {
        const expectedfavouriteNumber = "1"
        const expectedName = "Shalin"
        const updateArrayTransaction = await simpleStorage.addPerson(
            expectedfavouriteNumber,
            expectedName
        )
        await updateArrayTransaction.wait(1)
        const people = await simpleStorage.people(0)
        assert.equal(people[0], expectedfavouriteNumber)
        assert.equal(people[1], expectedName)
    })

    it("Should return favourite number mapped to a person", async function () {
        const testName = "Shalin"
        const expectedfavouriteNumber = "1"
        const updateStructTransaction = await simpleStorage.addPerson(
            expectedfavouriteNumber,
            testName
        )
        await updateStructTransaction.wait(1)
        const favouriteNumber = await simpleStorage.nameToFavouriteNumber(
            testName
        )
        assert.equal(favouriteNumber.toString(), expectedfavouriteNumber)
    })
})
