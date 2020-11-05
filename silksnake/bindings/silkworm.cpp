#pragma GCC diagnostic ignored "-Wattributes"

#include <pybind11/pybind11.h>

#define STRINGIFIED_VERSION_(x) #x
#define STRINGIFIED_VERSION(x) STRINGIFIED_VERSION_(x)

namespace py = pybind11;

void bind_block(py::module_& module);
void bind_chain_config(py::module_& module);
void bind_execution_processor(py::module_& module);
void bind_intra_block_state(py::module_& module);
void bind_remote_buffer(py::module_& module);
void bind_transaction(py::module_& module);
void bind_types(py::module_& module);

PYBIND11_MODULE(silkworm, module) {
    module.doc() = "Python binding for Silkworm";

    bind_block(module);
    bind_chain_config(module);
    bind_execution_processor(module);
    bind_intra_block_state(module);
    bind_remote_buffer(module);
    bind_transaction(module);
    bind_types(module);

#ifdef VERSION_INFO
    module.attr("__version__") = STRINGIFIED_VERSION(VERSION_INFO);
#else
    module.attr("__version__") = "dev";
#endif
}
