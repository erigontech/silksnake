#ifndef SILKSNAKE_BINDINGS_INTRA_BLOCK_STATE_H_
#define SILKSNAKE_BINDINGS_INTRA_BLOCK_STATE_H_

#include <ostream>

#include <silkworm/state/intra_block_state.hpp>

using namespace silkworm;

std::ostream& operator<<(std::ostream& out, const IntraBlockState& s);

#endif  // SILKSNAKE_BINDINGS_INTRA_BLOCK_STATE_H_
