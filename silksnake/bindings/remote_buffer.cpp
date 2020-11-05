#include <optional>
#include <sstream>

#include <pybind11/pybind11.h>
#include <silkworm/db/buffer.hpp>

#include "remote_buffer.hpp"
#include "types.hpp"

namespace py = pybind11;

using namespace silkworm;

std::ostream& operator<<(std::ostream& out, const RemoteBuffer& b) {
    out << &b;
    return out;
}

std::optional<Account> RemoteBuffer::read_account(const evmc::address& address) const noexcept {
    py::object data_value = state_reader_.attr("read_account_data")(address);
    py::print(py::str(data_value));
    return std::nullopt;
}

Bytes RemoteBuffer::read_code(const evmc::bytes32& code_hash) const noexcept {
    return {};
}

std::optional<BlockHeader> RemoteBuffer::read_header(uint64_t block_number, const evmc::bytes32& block_hash) const noexcept {
    return std::nullopt;
}

evmc::bytes32 RemoteBuffer::read_storage(const evmc::address& address, uint64_t incarnation, const evmc::bytes32& key) const noexcept {
    return {};
}

uint64_t RemoteBuffer::previous_incarnation(const evmc::address& address) const noexcept {
    py::object storage_value = state_reader_.attr("read_account_storage")(address);
    py::print(py::str(storage_value));
    return {};
}

void bind_remote_buffer(py::module_ &m) {
    py::class_<RemoteBuffer>(m, "RemoteBuffer")
        .def(py::init([](const py::handle state_reader) {
            py::print(state_reader);
            return RemoteBuffer(state_reader);
        }))
        .def("__repr__", [](const RemoteBuffer& b) {
            std::ostringstream oss;
            oss << "<silkworm::RemoteBuffer " << b << ">";
            return oss.str();
        });
}
