#ifndef SILKSNAKE_BINDINGS_PROCESSOR_H_
#define SILKSNAKE_BINDINGS_PROCESSOR_H_

#include <ostream>

#include <pybind11/pybind11.h>
#include <silkworm/execution/processor.hpp>

std::ostream& operator<<(std::ostream& out, const silkworm::ExecutionProcessor& p);

void bind_execution_processor(pybind11::module_& module);

#endif  // SILKSNAKE_BINDINGS_PROCESSOR_H_