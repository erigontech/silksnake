#include <optional>
#include <sstream>

#include <pybind11/pybind11.h>
#include <silkworm/db/buffer.hpp>

#include "remote_buffer.hpp"
#include "types.hpp"
#include "uint256_type_caster.hpp"

namespace py = pybind11;

using namespace silkworm;

std::ostream& operator<<(std::ostream& out, const RemoteBuffer& b) {
    out << &b;
    return out;
}

std::optional<Account> RemoteBuffer::read_account(const evmc::address& address) const noexcept {
    py::object silksnake_account = state_reader_.attr("read_account_data")(silkworm::to_hex(address));

    auto nonce = silksnake_account.attr("nonce").cast<uint64_t>();
    auto balance = silksnake_account.attr("balance").cast<intx::uint256>();
    auto incarnation = silksnake_account.attr("incarnation").cast<uint64_t>();
    auto code_hash = silkworm::to_bytes32(silkworm::from_hex(silksnake_account.attr("code_hash").cast<std::string>()));
    auto storage_root = silkworm::to_bytes32(silkworm::from_hex(silksnake_account.attr("storage_root").cast<std::string>()));

    return Account{nonce, balance, storage_root, code_hash, incarnation};
}

Bytes RemoteBuffer::read_code(const evmc::bytes32& code_hash) const noexcept {
    py::object silksnake_code = state_reader_.attr("read_code")(silkworm::to_hex(code_hash));
    auto code_string = std::string(py::str(silksnake_code));
    Bytes code_bytes{code_string.begin(), code_string.end()};
    return code_bytes;
}

std::optional<BlockHeader> RemoteBuffer::read_header(uint64_t block_number, const evmc::bytes32& block_hash) const noexcept {
    return std::nullopt;
}

evmc::bytes32 RemoteBuffer::read_storage(const evmc::address& address, uint64_t incarnation, const evmc::bytes32& key) const noexcept {
    py::object value = state_reader_.attr("read_account_storage")(silkworm::to_hex(address), incarnation, silkworm::to_hex(key));
    auto value_string = std::string(py::str(value));
    Bytes storage_value{value_string.begin(), value_string.end()};
    return silkworm::to_bytes32(storage_value);
}

uint64_t RemoteBuffer::previous_incarnation(const evmc::address& address) const noexcept {
    return 0;
}

void bind_remote_buffer(py::module_& module) {
    py::class_<RemoteBuffer>(module, "RemoteBuffer")
        .def(py::init([](const py::handle state_reader) {
            return RemoteBuffer{state_reader};
        }))
        .def("__repr__", [](const RemoteBuffer& b) {
            std::ostringstream oss;
            oss << "<silkworm::RemoteBuffer " << b << ">";
            return oss.str();
        });
}
