#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <optional>
#include <sstream>

#include <silkworm/types/transaction.hpp>

#include "uint256_type_caster.hpp"

namespace py = pybind11;

using namespace silkworm;

void bind_transaction(py::module_ &m) {
    py::class_<Transaction>(m, "Transaction")
        /*.def(py::init<
            uint64_t,                      // nonce
            intx::uint256,                 // gas_price
            uint64_t,                      // gas_limit
            std::optional<evmc::address>,  // to
            intx::uint256,                 // value
            Bytes,                         // data
            intx::uint256,                 // v
            intx::uint256,                 // r
            intx::uint256,                 // s
            std::optional<evmc::address>   // from
            >())*/
        .def(py::init([](
            uint64_t nonce,
            intx::uint256 gas_price,
            uint64_t gas_limit,
            std::optional<evmc::address> to,
            intx::uint256 value,
            std::string data_bytes, // use Pybind11 builtin type conversion from bytes to std::string
            intx::uint256 v,
            intx::uint256 r,
            intx::uint256 s,
            std::optional<evmc::address> from) {
                Bytes data(data_bytes.begin(), data_bytes.end()); // use C++ builtin conversion from char to uint8_t
                return Transaction{nonce, gas_price, gas_limit, to, value, data, v, r, s, from};
        }))
        .def_readwrite("nonce", &Transaction::nonce)
        .def_readwrite("gas_price", &Transaction::gas_price)
        .def_readwrite("gas_limit", &Transaction::gas_limit)
        .def_readwrite("to", &Transaction::to)
        .def_readwrite("value", &Transaction::value)
        .def_readwrite("data", &Transaction::data)
        .def_readwrite("v", &Transaction::v)
        .def_readwrite("r", &Transaction::r)
        .def_readwrite("s", &Transaction::s)
        .def_readwrite("from", &Transaction::from)
        .def("__repr__", [](const Transaction& t) {
            std::ostringstream oss;
            oss << "<silkworm::Transaction from="
                << " nonce=" << std::to_string(t.nonce)
                << " gas_price=(hi:" << t.gas_price.hi.hi << t.gas_price.hi.lo << " lo:" << t.gas_price.lo.hi << t.gas_price.lo.lo << ")"
                << " gas_limit=" << std::to_string(t.gas_limit)
                << " to="
                << " >";
            return oss.str();
        });
}
