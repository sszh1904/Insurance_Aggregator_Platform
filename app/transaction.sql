CREATE DATABASE IF NOT EXISTS `transaction` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `transaction`;

-- --------------------------------------------------------

--
-- Table structure for table `transaction`
--

DROP TABLE IF EXISTS `transaction`;
CREATE TABLE IF NOT EXISTS `transaction` (
  `trans_id` varchar(50) NOT NULL,
  `cust_nric` char(9) NOT NULL,
  `policy_creation_id` varchar(20) NOT NULL,
  `trans_datetime` varchar(30) NOT NULL,
  `amount` double(20,2) NOT NULL,
  PRIMARY KEY (`trans_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `transaction`
--

INSERT INTO `transaction` (`trans_id`, `cust_nric`, `policy_creation_id`, `trans_datetime`, `amount`) VALUES
('PAYID-MBW3RGQ9RR41344R4052994L', 'S9121381P', 'AIAPC329605', '2021-04-07T13:50:17Z', '200.00'),
('PAYID-MBW3T7Q9EN207184U299010B', 'S9121381P', 'AIAPC947367', '2021-04-07T13:56:14Z', '12.5'),
('PAYID-MBW3UYA4EN159377T811544Y', 'S9121381P', 'AVIVAPC808016', '2021-04-07T13:57:51Z', '100.0'),
('PAYID-MBZS3EA4G8095119T5698609', 'S9753582E', 'AVIVAPC532516', '2021-04-11T17:10:39Z', '100.0'),
('PAYID-MBZT4GQ1R11257839984053M', 'S9881237B', 'GEPC500506', '2021-04-11T18:21:13Z', '250.0'),
('PAYID-MBZUH4Q9X415629HJ841023X', 'S9881237B', 'AIAPC503480', '2021-04-11T18:46:09Z', '200.0'),
('PAYID-MBZUMSA0DT72212GW676822C', 'S9816407C', 'AIAPC123456', '2021-04-11T18:56:08Z', '280.0');
