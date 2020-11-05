#ifndef SILKSNAKE_BINDINGS_CHAIN_CONFIG_H_
#define SILKSNAKE_BINDINGS_CHAIN_CONFIG_H_

#include <pybind11/pybind11.h>
#include <silkworm/chain/config.hpp>

std::ostream& operator<<(std::ostream& out, const silkworm::ChainConfig& c);

void bind_chain_config(pybind11::module_& module);

#endif // SILKSNAKE_BINDINGS_CHAIN_CONFIG_H_