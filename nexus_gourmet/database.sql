SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema nexus_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `nexus_db` DEFAULT CHARACTER SET utf8 ;
USE `nexus_db` ;

-- -----------------------------------------------------
-- Table `nexus_db`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `nexus_db`.`users` ;

CREATE TABLE IF NOT EXISTS `nexus_db`.`users` (
  `cpf` VARCHAR(11) NOT NULL,
  `nome` VARCHAR(100) NOT NULL,
  `senha` VARCHAR(255) NOT NULL,
  `cargo` ENUM('ADMINISTRADOR', 'GARCOM', 'COZINHEIRO') NOT NULL DEFAULT 'GARCOM',
  `foto_usuario` VARCHAR(255) NULL,
  PRIMARY KEY (`cpf`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `nexus_db`.`tables`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `nexus_db`.`tables` ;

CREATE TABLE IF NOT EXISTS `nexus_db`.`tables` (
  `numero` INT NOT NULL,
  `capacidade` INT NOT NULL,
  `status` ENUM('LIVRE', 'OCUPADA') NOT NULL DEFAULT 'LIVRE',
  PRIMARY KEY (`numero`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `nexus_db`.`products`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `nexus_db`.`products` ;

CREATE TABLE IF NOT EXISTS `nexus_db`.`products` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(100) NOT NULL,
  `categoria` ENUM('BEBIDA', 'PRATO', 'SOBREMESA') NOT NULL,
  `preco` DECIMAL(10,2) NOT NULL,
  `tempo_preparacao` INT NOT NULL DEFAULT 15,
  `foto_prato` VARCHAR(255) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `nexus_db`.`orders`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `nexus_db`.`orders` ;

CREATE TABLE IF NOT EXISTS `nexus_db`.`orders` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `numero_diario` INT NOT NULL,
  `data_criacao` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `entrada_cozinha` DATETIME NULL,
  `saida_cozinha` DATETIME NULL,
  `status` ENUM('FINALIZADO', 'ENTREGUE', 'PRONTO', 'EM_PREPARO', 'CANCELADO', 'PENDENTE') NOT NULL DEFAULT 'PENDENTE',
  `numero_mesa` INT NOT NULL,
  `user_cpf` VARCHAR(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_orders_users_idx` (`user_cpf` ASC),
  INDEX `fk_orders_tables_idx` (`numero_mesa` ASC),
  CONSTRAINT `fk_orders_users`
    FOREIGN KEY (`user_cpf`)
    REFERENCES `nexus_db`.`users` (`cpf`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_orders_tables`
    FOREIGN KEY (`numero_mesa`)
    REFERENCES `nexus_db`.`tables` (`numero`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `nexus_db`.`itens_ordered`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `nexus_db`.`itens_ordered` ;

CREATE TABLE IF NOT EXISTS `nexus_db`.`itens_ordered` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `quantidade` INT NOT NULL DEFAULT 1,
  `observacao` VARCHAR(255) NULL,
  `cozinha_status` VARCHAR(20) NOT NULL DEFAULT 'PENDENTE',
  `preco_vendido` DECIMAL(10,2) NOT NULL DEFAULT 0.0,
  `order_id` INT NOT NULL,
  `product_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_itens_ordered_orders_idx` (`order_id` ASC),
  INDEX `fk_itens_ordered_products_idx` (`product_id` ASC),
  CONSTRAINT `fk_itens_ordered_orders`
    FOREIGN KEY (`order_id`)
    REFERENCES `nexus_db`.`orders` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_itens_ordered_products`
    FOREIGN KEY (`product_id`)
    REFERENCES `nexus_db`.`products` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;