#pragma GCC diagnostic ignored "-Wattributes"

#include <optional>
#include <sstream>

#include <pybind11/cast.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <silkworm/execution/processor.hpp>
#include <silkworm/types/transaction.hpp>

#define STRINGIFIED_VERSION_(x) #x
#define STRINGIFIED_VERSION(x) STRINGIFIED_VERSION_(x)

namespace py = pybind11;

void bind_block(py::module_ &m);
void bind_buffer(py::module_ &m);
void bind_intra_block_state(py::module_ &m);
void bind_transaction(py::module_ &m);
void bind_types(py::module_ &m);
//void bind_execution_processor(py::module_ &m);

PYBIND11_MODULE(silkworm, m) {
    m.doc() = "Python binding for Silkworm";

    bind_block(m);
    bind_buffer(m);
    bind_intra_block_state(m);
    bind_transaction(m);
    bind_types(m);
    //bind_execution_processor(m);

#ifdef VERSION_INFO
    m.attr("__version__") = STRINGIFIED_VERSION(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
