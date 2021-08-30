CREATE DATABASE IF NOT EXISTS `agent` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `agent`;

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `agent`;
CREATE TABLE IF NOT EXISTS `agent` (
    `agent_name` varchar(64) NOT NULL,
    `agent_id` varchar (10) NOT NULL,
    `agent_nric` varchar(9) NOT NULL,
    `agent_password` varchar(100) NOT NULL,
    PRIMARY KEY (`agent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `agentcustomer`;
CREATE TABLE IF NOT EXISTS `agentcustomer` (
  `agent_id` varchar (10) NOT NULL,
  `cust_nric` varchar (9) NOT NULL,
  PRIMARY KEY(`agent_id`, `cust_nric`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `agent` (`agent_name`,`agent_id`,`agent_nric`,`agent_password`) VALUES
('Samuel','001',"S1234567A", 'sam123'),
('Leonard','002',"S1234567B",'leo123'),
('Dave','003',"S1234567C", 'dave123');
COMMIT;

INSERT INTO `agentcustomer` (`agent_id`,`cust_nric`) 
VALUES ('001','S9121381P'),
('001','S9753582E'),
('001','S9832585S'),
('002','S9881237B'),
('002','S9816407C'),
('002','S9054355M');

COMMIT;
