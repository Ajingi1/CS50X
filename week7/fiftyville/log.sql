-- Keep a log of any SQL queries you execute as you solve the mystery.

sqlite3 fiftyville.db -- run sqlite3
sqlite> .tables -- run this command to learn tables in the database
-- airports              crime_scene_reports   people
-- atm_transactions      flights               phone_calls
-- bakery_security_logs  interviews
-- bank_accounts         passengers
sqlite> .schema crime_scene_reports -- run this command to learn the crime_scene_reports table collumn names
    -- id INTEGER,
    -- year INTEGER,
    -- month INTEGER,
    -- day INTEGER,
    -- street TEXT,
    -- description TEXT,
    -- PRIMARY KEY(id)

sqlite> SELECT description
   ...> FROM crime_scene_reports
   ...> WHERE month = 7
   ...> AND day = 28 AND street = 'Humphrey Street'; -- learn report from the crime scene

    -- The description
    -- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
    -- Interviews were conducted today with three witnesses who were present at the time –
    -- each of their interview transcripts mentions the bakery. |
    -- Littering took place at 16:36. No known witnesses.

sqlite> SELECT * FROM interviews
   ...> WHERE month = 7
   ...> AND day = 28;
   -- From the transcription we learn that the thief enter car from bakery parking lot and drive away
   -- the thief escape from the bakery 10 after the thief mean 10:25 am

-- key from the data that we collect now
-- month = 7
-- day = 28
-- street = 'Humphrey Street'
-- escape time frame is 10:15 to 10:25


-- ######### The start of the 3 people that give information about the thief #######
-- Ruth : Sometime within ten minutes of the theft,
--        I saw the thief get into a car in the bakery parking lot and drive away.
--       If you have security footage from the bakery parking lot,
--       you might want to look for cars that left the parking lot in that time frame.

-- Let us see the cars that left the place at the time frame and the name of the car drivers.
sqlite> SELECT name, bakery_security_logs.license_plate FROM people
   ...> JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate
   ...> WHERE month = 7 AND day = 28 AND hour = 10 AND minute < 25 AND activity = 'exit';
-- +---------+---------------+
-- |  name   | license_plate |
-- +---------+---------------+
-- | Vanessa | 5P2BI95       |
-- | Bruce   | 94KL13X       |
-- | Barry   | 6P58WS2       |
-- | Luca    | 4328GD8       |
-- | Sofia   | G412CB7       |
-- | Iman    | L93JTIZ       |
-- | Diana   | 322W7JE       |
-- | Kelsey  | 0NTHK55       |
-- +---------+---------------+

-- suspect from Ruth explanation are 8 people that left the bakery at the time frame
-- Vanessa, Bruce, Barry, Luca, Sofia, Iman, Diana, Kelsey


-- Eugene :Idon't know the thief's name, but it was someone I recognized.
--        Earlier this morning, before I arrived at Emma's bakery,
--        I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.
sqlite> SELECT month, day, bank_accounts.account_number, name, transaction_type
   ...> FROM atm_transactions
   ...> JOIN bank_accounts ON atm_transactions.account_number = bank_accounts.account_number
   ...> JOIN people ON bank_accounts.person_id = people.id
   ...> WHERE month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';
-- +-------+-----+----------------+---------+------------------+
-- | month | day | account_number |  name   | transaction_type |
-- +-------+-----+----------------+---------+------------------+
-- | 7     | 28  | 49610011       | Bruce   | withdraw         |
-- | 7     | 28  | 26013199       | Diana   | withdraw         |
-- | 7     | 28  | 16153065       | Brooke  | withdraw         |
-- | 7     | 28  | 28296815       | Kenny   | withdraw         |
-- | 7     | 28  | 25506511       | Iman    | withdraw         |
-- | 7     | 28  | 28500762       | Luca    | withdraw         |
-- | 7     | 28  | 76054385       | Taylor  | withdraw         |
-- | 7     | 28  | 81061156       | Benista | withdraw         |
-- +-------+-----+----------------+---------+------------------+
-- The people that are in the list of Ruth suspect and Eugene suspect
-- Bruce, Luca, Iman and Diana

                                                                                   |
-- Raymond : As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
--        In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
--        The thief then asked the person on the other end of the phone to purchase the flight ticket.

sqlite> SELECT name , people.phone_number FROM people
    JOIN phone_calls ON people.phone_number = phone_calls.caller
    WHERE day = 28 AND month = 7 AND duration < 60;
-- +---------+----------------+
-- |  name   |  phone_number  |
-- +---------+----------------+
-- | Sofia   | (130) 555-0289 |
-- | Kelsey  | (499) 555-9472 |
-- | Bruce   | (367) 555-5533 |
-- | Kelsey  | (499) 555-9472 |
-- | Taylor  | (286) 555-6063 |
-- | Diana   | (770) 555-1861 |
-- | Carina  | (031) 555-6622 |
-- | Kenny   | (826) 555-1652 |
-- | Benista | (338) 555-6650 |
-- +---------+----------------+
-- suspect from Raymond interview who are also in the suspects from above 2 interview
-- Bruce, Diana

-- Now let us check the tommorrow's earliest flight
sqlite> SELECT flights.id, flights.origin_airport_id, flights.destination_airport_id, flights.day,flights.hour, airports.city, airports.full_name
   ...> FROM flights
   ...> JOIN airports ON airports.id = flights.destination_airport_id
   ...> WHERE day = 29 AND month = 7 ORDER BY hour;
-- +----+-------------------+------------------------+-----+------+---------------+-------------------------------------+
-- | id | origin_airport_id | destination_airport_id | day | hour |     city      |              full_name              |
-- +----+-------------------+------------------------+-----+------+---------------+-------------------------------------+
-- | 36 | 8                 | 4                      | 29  | 8    | New York City | LaGuardia Airport                   |
-- | 43 | 8                 | 1                      | 29  | 9    | Chicago       | O'Hare International Airport        |
-- | 23 | 8                 | 11                     | 29  | 12   | San Francisco | San Francisco International Airport |
-- | 53 | 8                 | 9                      | 29  | 15   | Tokyo         | Tokyo International Airport         |
-- | 18 | 8                 | 6                      | 29  | 16   | Boston        | Logan International Airport         |
-- +----+-------------------+------------------------+-----+------+---------------+-------------------------------------+

-- Now we know that tommorrow's first flight is flight to New York city
-- that means the thief and his friend escape to New York City
-- ############# The end of the interview #################
-- We have 2 suspects  Bruce, Diana


-- ##### Now from the information we extract frmo the above information let us list key words and find the thief ########
-- #### KEY WORDS ####
-- Escape City = New York City - Airport_id = 4
-- Origin city = Fiftyville - Airport_id = 8
-- suspect Bruce and Diana
-- flights id = 36

 SELECT name FROM passengers JOIN people ON people.passport_number = passengers.passport_number JOIN flights ON flights.id = flight_id
   ...> WHERE destination_airport_id = 4 AND origin_airport_id = 8 AND day = 29 AND month = 7 AND hour = 8 AND name IN
   ...> (SELECT name FROM people JOIN phone_calls ON people.phone_number = phone_calls.caller
   ...>  WHERE day = 28 AND month = 7 AND duration < 60 AND name IN
   ...> (SELECT name FROM atm_transactions
   ...> JOIN bank_accounts ON atm_transactions.account_number = bank_accounts.account_number JOIN people ON bank_accounts.person_id = people.id
   ...> WHERE month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw' AND name IN
   ...> (SELECT name FROM people JOIN phone_calls ON people.phone_number = phone_calls.caller
   ...> WHERE day = 28 AND month = 7 AND duration < 60)));
-- +--------+
-- |  name  |
-- +--------+
-- | Bruce  |
-- | Taylor |
-- | Kenny  |
-- +--------+
-- ##### Our thief is Bruce #####

-- Now let us check with who bruce speak

SELECT name, caller, receiver, people.phone_number FROM people
   ...> JOIN phone_calls ON people.phone_number = phone_calls.caller
   ...> WHERE day = 28 AND month = 7 AND duration < 60 AND people.name = 'Bruce';
-- +-------+----------------+----------------+----------------+
-- | name  |     caller     |    receiver    |  phone_number  |
-- +-------+----------------+----------------+----------------+
-- | Bruce | (367) 555-5533 | (375) 555-8161 | (367) 555-5533 |
-- +-------+----------------+----------------+----------------+
-- The number that bruce call is (375) 555-8161 let us check who this number belong to

sqlite> SELECT name FROM people WHERE people.phone_number = '(375) 555-8161';
-- +-------+
-- | name  |
-- +-------+
-- | Robin |
-- +-------+

-- Robin is the person that Bruce called
