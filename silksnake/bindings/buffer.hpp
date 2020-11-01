#ifndef SILKSNAKE_BINDINGS_BUFFER_H_
#define SILKSNAKE_BINDINGS_BUFFER_H_

#include <ostream>

#include <silkworm/db/buffer.hpp>

using namespace silkworm;

std::ostream& operator<<(std::ostream& out, const db::Buffer& s);

#endif  // SILKSNAKE_BINDINGS_BUFFER_H_
