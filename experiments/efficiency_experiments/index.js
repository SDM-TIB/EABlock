const parser = require('rocketrml');

const doMapping = async () => {
  const options = {
    toRDF: true,
    verbose: true,
    xmlPerformanceMode: false,
    replace: false,
  };
  const result = await parser.parseFile('/efficiency_exp_data/noORM_2k_baseline.ttl', '/efficiency_exp_data/noORM_2k_baseline.nt', options).catch((err) => { console.log(err); });
  //const result = await parser.parseFile('/efficiency_exp_data/EABlock/transfered_mapping.ttl', '/efficiency_exp_data/EABlock/noORM_1k_EABlock.nt', options).catch((err) => { console.log(err); });
  console.log(result);
};

doMapping();
