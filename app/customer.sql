CREATE DATABASE IF NOT EXISTS `customer` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `customer`;

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `customer`;
CREATE TABLE IF NOT EXISTS `customer` (
  `cust_name` varchar(64) NOT NULL,
  `cust_nric` char(9) NOT NULL,
  `cust_sex` char(1) NOT NULL,
  `cust_dob` varchar(20) NOT NULL,
  `cust_email` varchar(100) NOT NULL,
  `cust_password` varchar(20) NOT NULL,
  `mobile_no` varchar(15),
  `address` varchar(100),
  `agent_id` varchar(100) NOT NULL,
  PRIMARY KEY (`cust_nric`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `cust_policies`;
CREATE TABLE IF NOT EXISTS `cust_policies` (
  `cust_nric` varchar (9) NOT NULL,
  `policy_id` varchar (100) NOT NULL,
  `policy_creation_id` varchar(100) NOT NULL,
  `policy_name` varchar(100) NOT NULL,
  `policy_category` varchar(100) NOT NULL,
  `monthly_premium` varchar(100) NOT NULL,
  `coverage` varchar(100),
  `sum_insured` varchar(100),
  `num_condition_covered` varchar(100),
  `rate_of_return_per_annum` varchar(100),
  `initial_deposit` varchar(100),
  PRIMARY KEY(`cust_nric`,`policy_creation_id`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- Dumping data for customer -- 
INSERT INTO `customer` (`cust_name`,`cust_nric`,`cust_sex`, `cust_dob`, `cust_email`, `cust_password`, `mobile_no`, `address`, `agent_id`) VALUES
('PHAY LI YAN','S9121381P', 'F', '1998-11-21', 'liyan@gmail.com', 'ly123', '98568988', 'TECK WHYE STREET 13 09-111 S(601288)', '001');
INSERT INTO `customer` (`cust_name`,`cust_nric`,`cust_sex`, `cust_dob`, `cust_email`, `cust_password`, `mobile_no`, `address`, `agent_id`) VALUES
('ROYCE TEO KAI EN','S9753582E', 'M', '1959-01-12', 'royce@gmail.com', 'royce123', '97591232', 'CLEMENTI STREET 11 21-369 S(653288)', '001');
INSERT INTO `customer` (`cust_name`,`cust_nric`,`cust_sex`, `cust_dob`, `cust_email`, `cust_password`, `mobile_no`, `address`, `agent_id`) VALUES
('SINDHU NAIDU','S9832585S', 'F', '1950-02-06', 'sindu@gmail.com', 'sindhu123', '98589637', 'PAYA LEBAR STREET 58 23-10 S(520138)', '001');
INSERT INTO `customer` (`cust_name`,`cust_nric`,`cust_sex`, `cust_dob`, `cust_email`, `cust_password`, `mobile_no`, `address`, `agent_id`) VALUES
('BRYAN WONG CHU SHENG','S9881237B', 'M', '1998-07-19', 'bryan.wong@gmail.com', 'bryan123', '99544547', 'KOVAN AVENUE 2 02-113 S(822101)', '002');
INSERT INTO `customer` (`cust_name`,`cust_nric`,`cust_sex`, `cust_dob`, `cust_email`, `cust_password`, `mobile_no`, `address`, `agent_id`) VALUES
('IAN KOH','S9816407C', 'M', '1998-05-02', 'ianiscold@hotmail.com', 'iankoh123', '95566234', 'ORCHARD ROAD 07-896 S(689124)', '002');
INSERT INTO `customer` (`cust_name`,`cust_nric`,`cust_sex`, `cust_dob`, `cust_email`, `cust_password`, `mobile_no`, `address`, `agent_id`) VALUES
('TAN XIAO MING','S9054355M', 'M', '1990-02-01', 'xiaoming@gmail.com', 'xm123', '91214523', 'PASIR RIS AVENUE 6 03-258 S(609774)', '002');


-- Dumping data for policies bought by each customer -- 
INSERT INTO `cust_policies` (`cust_nric`,`policy_id`,`policy_creation_id`,`policy_name`,`policy_category`,`monthly_premium`,`coverage`, `sum_insured`,`num_condition_covered`,`rate_of_return_per_annum`,`initial_deposit`) VALUES
('S9121381P', 'AIAS2', 'AIAPC329605', 'AIA Smart Reward Saver II', 'Savings', '200.0', null, null, null, '1.0', '300.0');

INSERT INTO `cust_policies` (`cust_nric`,`policy_id`,`policy_creation_id`,`policy_name`,`policy_category`,`monthly_premium`,`coverage`, `sum_insured`,`num_condition_covered`,`rate_of_return_per_annum`,`initial_deposit`) VALUES
('S9121381P', 'AIACI2', 'AIAPC947367', 'AIA Power Critical Cover Value Plan', 'Critical Illness', '12.5', null, '30000.0', '150', null, null);

INSERT INTO `cust_policies` (`cust_nric`,`policy_id`,`policy_creation_id`,`policy_name`,`policy_category`,`monthly_premium`,`coverage`, `sum_insured`,`num_condition_covered`,`rate_of_return_per_annum`,`initial_deposit`) VALUES
('S9121381P','AVIVAWL1','AVIVAPC808016','Aviva MyWholeLifePlan III', 'Whole Life', '100.0', 'Death, TI', '30000.0', null, null, null);

INSERT INTO `cust_policies` (`cust_nric`,`policy_id`,`policy_creation_id`,`policy_name`,`policy_category`,`monthly_premium`,`coverage`, `sum_insured`,`num_condition_covered`,`rate_of_return_per_annum`,`initial_deposit`) VALUES
('S9753582E','AVIVAWL5','AVIVAPC532516','Aviva MyWholeLifePlan I', 'Whole Life','100.0', 'Death', '12000.0', null, null, null);

INSERT INTO `cust_policies` (`cust_nric`,`policy_id`,`policy_creation_id`,`policy_name`,`policy_category`,`monthly_premium`,`coverage`, `sum_insured`,`num_condition_covered`,`rate_of_return_per_annum`,`initial_deposit`) VALUES
('S9881237B', 'GES1', 'GEPC500506', 'Great Savings', 'Savings', '250.0', null, null, null, '1.0', '300.0');

INSERT INTO `cust_policies` (`cust_nric`,`policy_id`,`policy_creation_id`,`policy_name`,`policy_category`,`monthly_premium`,`coverage`, `sum_insured`,`num_condition_covered`,`rate_of_return_per_annum`,`initial_deposit`) VALUES
('S9881237B', 'AIAS2', 'AIAPC503480', 'AIA Smart Reward Saver II', 'Savings', '200.0', null, null, null, '1.0', '300.0');

INSERT INTO `cust_policies` (`cust_nric`,`policy_id`,`policy_creation_id`,`policy_name`,`policy_category`,`monthly_premium`,`coverage`, `sum_insured`,`num_condition_covered`,`rate_of_return_per_annum`,`initial_deposit`) VALUES
('S9816407C', 'AIAS3', 'AIAPC123456', 'AIA Smart Flexi Rewards', 'Savings', '280.0', null, null, null, '3.0', '450.0');

COMMIT;
