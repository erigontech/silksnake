#ifndef SILKSNAKE_BINDINGS_INTRA_BLOCK_STATE_H_
#define SILKSNAKE_BINDINGS_INTRA_BLOCK_STATE_H_

#include <ostream>

#include <pybind11/pybind11.h>
#include <silkworm/state/intra_block_state.hpp>

std::ostream& operator<<(std::ostream& out, const silkworm::IntraBlockState& s);

void bind_intra_block_state(pybind11::module_& module);

#endif  // SILKSNAKE_BINDINGS_INTRA_BLOCK_STATE_H_
