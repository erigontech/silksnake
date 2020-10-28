#include <pybind11/cast.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <optional>
#include <sstream>

#include <silkworm/execution/processor.hpp>
#include <silkworm/types/transaction.hpp>

#define STRINGIFIED_VERSION_(x) #x
#define STRINGIFIED_VERSION(x) STRINGIFIED_VERSION_(x)

intx::uint256 test_uint256(intx::uint256 v)
{
    return v;
}

namespace py = pybind11;

void bind_transaction(py::module_ &m);
//void bind_execution_processor(py::module_ &m);

PYBIND11_MODULE(silkworm, m) {
    m.doc() = "Python binding for Silkworm";

    m.def("test_uint256", &test_uint256, "test_uint256 function");

    bind_transaction(m);
    //bind_execution_processor(m);

#ifdef VERSION_INFO
    m.attr("__version__") = STRINGIFIED_VERSION(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
