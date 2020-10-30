#ifndef SILKSNAKE_BINDINGS_TRANSACTION_H_
#define SILKSNAKE_BINDINGS_TRANSACTION_H_

#include <ostream>

#include <silkworm/types/transaction.hpp>

using namespace silkworm;

std::ostream& operator<<(std::ostream& out, const Transaction& t);

#endif  // SILKSNAKE_BINDINGS_TRANSACTION_H_