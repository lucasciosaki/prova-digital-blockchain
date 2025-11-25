const hre = require("hardhat");

async function main() {
  console.log("Preparando para compilar e implantar...");

  const RegistryFactory = await hre.ethers.getContractFactory("Prova_Digital");

  console.log("Implantando Prova_Digital...");
  const registry = await RegistryFactory.deploy(); 

  await registry.waitForDeployment();

  const contractAddress = await registry.getAddress();
  
  console.log(`✅ Sucesso! Contrato Prova_Digital implantado em: ${contractAddress}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});