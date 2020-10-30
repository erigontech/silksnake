#ifndef SILKSNAKE_BINDINGS_TYPES_H_
#define SILKSNAKE_BINDINGS_TYPES_H_

#include <ostream>

#include <evmone/evmc/include/evmc/evmc.hpp>

std::ostream& operator<<(std::ostream& out, intx::uint256 i);
std::ostream& operator<<(std::ostream& out, const evmc::address& a);
std::ostream& operator<<(std::ostream& out, const evmc::bytes32& b);

#endif  // SILKSNAKE_BINDINGS_TYPES_H_