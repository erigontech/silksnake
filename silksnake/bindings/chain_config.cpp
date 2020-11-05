#include <sstream>

#include "chain_config.hpp"

using namespace silkworm;

std::ostream& operator<<(std::ostream& out, const ChainConfig& c) {
    out << "chain_id=" << c.chain_id
        << " dao_block=" << c.dao_block.value_or(-1)
        << " ripemd_deletion_block=" << c.ripemd_deletion_block.value_or(-1)
        << " homestead_block=" << c.homestead_block.value_or(-1)
        << " tangerine_whistle_block=" << c.tangerine_whistle_block.value_or(-1)
        << " spurious_dragon_block=" << c.spurious_dragon_block.value_or(-1)
        << " byzantium_block=" << c.byzantium_block.value_or(-1)
        << " constantinople_block=" << c.constantinople_block.value_or(-1)
        << " petersburg_block=" << c.petersburg_block.value_or(-1)
        << " istanbul_block=" << c.istanbul_block.value_or(-1)
        << " muir_glacier_block=" << c.muir_glacier_block.value_or(-1);
    return out;
}

void bind_chain_config(pybind11::module_& module) {
    pybind11::class_<ChainConfig>(module, "ChainConfig")
        .def(pybind11::init([](uint64_t chain_id){
            return *lookup_chain_config(chain_id);
        }))
        .def("__repr__", [](const ChainConfig& c) {
            std::ostringstream oss;
            oss << "<silkworm::ChainConfig " << c << ">";
            return oss.str();
        });
}
