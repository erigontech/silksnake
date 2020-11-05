#ifndef SILKSNAKE_BINDINGS_TRANSACTION_H_
#define SILKSNAKE_BINDINGS_TRANSACTION_H_

#include <ostream>

#include <pybind11/pybind11.h>
#include <silkworm/types/transaction.hpp>

std::ostream& operator<<(std::ostream& out, const silkworm::Transaction& t);

void bind_transaction(pybind11::module_& module);

#endif  // SILKSNAKE_BINDINGS_TRANSACTION_H_