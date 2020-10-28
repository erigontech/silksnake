#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <intx/intx.hpp>

namespace pybind11 { namespace detail {
    template <> struct type_caster<intx::uint256> {
        static constexpr int bytes32 = sizeof(intx::uint256);
    public:
        /**
         * This macro establishes the name 'uint256' in function signatures and declares a local variable
         * 'value' of type intx::uint256.
         */
        PYBIND11_TYPE_CASTER(intx::uint256, _("uint256"));

        /**
         * Conversion part 1 (Python -> C++): convert a Python object into a intx::uint256 instance or return false
         * upon failure. The second argument indicates whether implicit conversions should be applied.
         */
        bool load(handle src, bool) {
            /* Extract PyObject from handle */
            PyObject *source = src.ptr();
            /* Try converting into a Python integer value */
            PyObject *tmp = PyNumber_Long(source);
            if (!tmp) {
                return false;
            }
            /* Now try to convert into a C++ intx::uint256 using a big-endian intermediate buffer */
            PyLongObject *pylong_tmp = (PyLongObject *)tmp;
            //constexpr auto bytes32 = sizeof(intx::uint256);
            uint8_t buffer[bytes32];
            int little_endian = 0;
            int is_signed = 0;
            int rv = _PyLong_AsByteArray(pylong_tmp, (unsigned char *)buffer, bytes32, little_endian, is_signed);
            if (rv == -1) {
                return false;
            }
            value = intx::be::load<intx::uint256>(buffer);
            Py_DECREF(tmp);
            /* Ensure return code was OK (to avoid out-of-range errors etc) */
            return !(value == -1 && !PyErr_Occurred());
        }

        /**
         * Conversion part 2 (C++ -> Python): convert an intx::uint256 instance into a Python object. The second and
         * third arguments are used to indicate the return value policy and parent object and are generally ignored
         * by implicit casters.
         */
        static handle cast(intx::uint256 src, return_value_policy /* policy */, handle /* parent */) {
            //constexpr auto bytes32 = sizeof(intx::uint256);
            uint8_t buffer[bytes32];
            intx::be::store(buffer, src);
            int little_endian = 0;
            int is_signed = 0;
            return _PyLong_FromByteArray(buffer, bytes32, little_endian, is_signed);
        }
    };
}} // namespace pybind11::detail
